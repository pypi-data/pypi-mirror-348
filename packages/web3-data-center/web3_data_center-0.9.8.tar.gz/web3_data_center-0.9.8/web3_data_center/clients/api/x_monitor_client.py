from .base_api_client import BaseAPIClient
from .endpoint_config import EndpointConfig
from ..mixins import AuthMixin, RateLimitMixin, ConfigMixin
from ..mixins.auth import AuthType
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime, timezone

import json

import aiohttp
import logging

logger = logging.getLogger(__name__)

class XMonitorClient(BaseAPIClient, ConfigMixin, AuthMixin, RateLimitMixin):
    """XMonitor API client"""

    ENDPOINTS = {
        'add_account': EndpointConfig(
            path="/api",
            batch_size=50,
            rate_limit=3.0,
            cost_weight=2.0
        ),
        'remove_account': EndpointConfig(
            path="/api",
            batch_size=20,
            rate_limit=5.0
        ),
        'account_txlist': EndpointConfig(
            path="/api",
            batch_size=100,
            rate_limit=5.0
        ),
        'account_tokentx': EndpointConfig(
            path="/api",
            batch_size=100,
            rate_limit=5.0
        ),
        'account_nfttx': EndpointConfig(
            path="/api",
            batch_size=100,
            rate_limit=5.0
        ),
        'account_internal_txs': EndpointConfig(
            path="/api",
            batch_size=100,
            rate_limit=5.0
        )
    }    

    def __init__(self, config_path: str = "config.yml", use_proxy: bool = True):
        """Initialize XMonitor client"""
        super().__init__("x_monitor", config_path, use_proxy)
        # Setup authentication and rate limits
        self.setup_auth(AuthType.API_KEY)
        self.setup_rate_limits(self.ENDPOINTS)


    async def setup(self):
        self.initialization_time = datetime.now(timezone.utc)
        self.last_check_time = self.initialization_time
        self.user_auth_token = self.api_config['auth_token']
        self.list_id = self.api_config['list_id']
        self.add_route = self.api_config['add_route']
        self.remove_route = self.api_config['remove_route']
        self.list_route = self.api_config['list_route']
        self.timeline_route = self.api_config['timeline_route']
        self.query_id = self.api_config['query_id']
        logger.info(f"Initialized XMonitor. Last check time set to {self.last_check_time}")
        self._user_id_cache: Dict[str, str] = {}  # Cache for user IDs: screen_name -> user_id
        self.monitored_accounts = {}
        self.processed_tweets = []  # List of processed tweet IDs to avoid duplicates
        await self.initialize_list_members()

    @RateLimitMixin.rate_limited('add_account')
    async def add_account(self, screen_name: str) -> bool:
        user_id = await self.get_user_id(screen_name)
        if not user_id:
            logger.warning(f"Failed to add {screen_name} to monitored accounts. User ID not found.")
            return False
        print(f"{screen_name} Monitored accounts: {self.monitored_accounts}")
        if screen_name in self.monitored_accounts:
            logger.info(f"{screen_name} is already in monitored accounts with ID: {self.monitored_accounts[screen_name]}")
            return False
        
        result = await self._add_member_to_list(user_id)
        if self._is_operation_successful(result):
            self.monitored_accounts[screen_name] = user_id
            logger.info(f"Added {screen_name} (ID: {user_id}) to monitored accounts and the Twitter list.")
            return True
        return False

    @RateLimitMixin.rate_limited('remove_account')
    async def remove_account(self, screen_name: str) -> bool:
        if screen_name not in self.monitored_accounts:
            logger.warning(f"{screen_name} is not in monitored accounts.")
            return False

        user_id = self.monitored_accounts[screen_name]
        result = await self._remove_member_from_list(user_id)
        if self._is_operation_successful(result):
            del self.monitored_accounts[screen_name]
            logger.info(f"Removed {screen_name} (ID: {user_id}) from monitored accounts and the Twitter list.")
            return True
        return False

    async def _add_member_to_list(self, user_id: str) -> Dict[str, Any]:
        if not self.add_route:
            raise ValueError("add_route is not initialized")
        if not self.user_auth_token:
            raise ValueError("user_auth_token is not initialized")
        if not self.query_id:
            raise ValueError("query_id is not initialized")
        if not self.list_id:
            raise ValueError("list_id is not initialized")
        endpoint = f"/graphql/{self.add_route}/ListAddMember"
        payload = self._get_list_operation_payload(user_id)
        headers = self.headers.copy()
        
        _, headers = await self.authenticate_request("POST", endpoint, {}, headers, payload)
        # Add Twitter-specific auth token
        headers["AuthToken"] = self.user_auth_token
        return await self._make_request(method="POST", endpoint=endpoint, data=payload, headers=headers)

    async def _remove_member_from_list(self, user_id: str) -> Dict[str, Any]:
        if not self.remove_route:
            raise ValueError("remove_route is not initialized")
        if not self.user_auth_token:
            raise ValueError("user_auth_token is not initialized")
        if not self.query_id:
            raise ValueError("query_id is not initialized")
        if not self.list_id:
            raise ValueError("list_id is not initialized")
        endpoint = f"/graphql/{self.remove_route}/ListRemoveMember"
        payload = self._get_list_operation_payload(user_id)
        headers = self.headers.copy()
        
        _, headers = await self.authenticate_request("POST", endpoint, {}, headers, payload)
        # Add Twitter-specific auth token
        headers["AuthToken"] = self.user_auth_token
        return await self._make_request(method="POST", endpoint=endpoint, data=payload, headers=headers)

    def _get_list_operation_payload(self, user_id: str) -> Dict[str, Any]:
        return {
            "variables": {"listId": self.list_id, "userId": user_id},
            "features": {
                "rweb_tipjar_consumption_enabled": True,
                "responsive_web_graphql_exclude_directive_enabled": True,
                "verified_phone_label_enabled": False,
                "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                "responsive_web_graphql_timeline_navigation_enabled": True
            },
            "queryId": self.query_id
        }

    def _is_operation_successful(self, result: Optional[Dict[str, Any]]) -> bool:
        if result is None:
            return False
        if isinstance(result, dict):
            if 'error' in result:
                logger.error(f"API Error: {result['error']}")
                return False
            if 'data' in result and isinstance(result['data'], dict) and 'list' in result['data']:
                return True
        logger.warning(f"Unexpected API response: {result}")
        return False

    async def check_for_new_posts(self):
        if not self.timeline_route:
            raise ValueError("timeline_route is not initialized")
        if not self.list_id:
            raise ValueError("list_id is not initialized")
        logger.info("Checking for new posts...")
        current_time = datetime.now(timezone.utc)
        new_posts = []
        try:
            endpoint = f"/graphql/{self.timeline_route}/ListLatestTweetsTimeline"
            variables = {
                "listId": self.list_id,
                "count": 5,
                "cursor": None  # Add cursor handling if needed
            }
            features = {
                "rweb_tipjar_consumption_enabled": True,
                "responsive_web_graphql_exclude_directive_enabled": True,
                "verified_phone_label_enabled": False,
                "creator_subscriptions_tweet_preview_api_enabled": True,
                "responsive_web_graphql_timeline_navigation_enabled": True,
                "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                "communities_web_enable_tweet_community_results_fetch": True,
                "c9s_tweet_anatomy_moderator_badge_enabled": True,
                "articles_preview_enabled": True,
                "responsive_web_edit_tweet_api_enabled": True,
                "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
                "view_counts_everywhere_api_enabled": True,
                "longform_notetweets_consumption_enabled": True,
                "responsive_web_twitter_article_tweet_consumption_enabled": True,
                "tweet_awards_web_tipping_enabled": False,
                "creator_subscriptions_quote_tweet_preview_enabled": False,
                "freedom_of_speech_not_reach_fetch_enabled": True,
                "standardized_nudges_misinfo": True,
                "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
                "rweb_video_timestamps_enabled": True,
                "longform_notetweets_rich_text_read_enabled": True,
                "longform_notetweets_inline_media_enabled": True,
                "responsive_web_enhance_cards_enabled": False
            }
            params = {
                "variables": json.dumps(variables),
                "features": json.dumps(features)
            }
            
            params, headers = await self.authenticate_request("GET", endpoint, params, self.headers)
            response = await self._make_request(method="GET", endpoint=endpoint, params=params, headers=headers)
            if response:
                instructions = response.get('data', {}).get('list', {}).get('tweets_timeline', {}).get('timeline', {}).get('instructions', [])
                for instruction in instructions:
                    if instruction.get('type') == 'TimelineAddEntries':
                        entries = instruction.get('entries', [])
                        for entry in entries:
                                tweet = entry.get('content', {}).get('itemContent', {}).get('tweet_results', {}).get('result', {})
                                if tweet:
                                    tweet_id = tweet.get('rest_id')
                                    if tweet_id is None:
                                        continue
                                created_at = datetime.strptime(tweet.get('legacy', {}).get('created_at', 'Tue Sep 03 23:22:54 +0000 2024'), '%a %b %d %H:%M:%S +0000 %Y').replace(tzinfo=timezone.utc)
                                # print(created_at, self.initialization_time, tweet_id)
                                if created_at > self.last_check_time and tweet_id not in self.processed_tweets:
                                    self.processed_tweets.append(tweet_id)
                                    legacy = tweet.get('legacy', {})
                                    user = tweet.get('core', {}).get('user_results', {}).get('result', {}).get('legacy', {})
                                                                                # Get the tweet text and URLs
                                    text = legacy.get('full_text', '')
                                    urls = legacy.get('entities', {}).get('urls', [])
                                            # Replace shortened URLs with expanded ones
                                    for url in urls:
                                        short_url = url.get('url', '')
                                        expanded_url = url.get('expanded_url', '')
                                        if short_url and expanded_url:
                                            text = text.replace(short_url, expanded_url)
                                            new_post = {
                                                'id': tweet_id,
                                                'text': text,
                                                'user': user.get('screen_name'),
                                                'created_at': created_at
                                            }
                                            new_posts.append(new_post)
                                            logger.debug(f"New post added: {new_post}")
                self.last_check_time = current_time
            else:
                logger.error("Failed to fetch new posts.")
            
            logger.info(f"Found {len(new_posts)} new posts")
        except Exception as e:
            logger.error(f"Error checking for new posts: {str(e)}")
            logger.exception("Exception details:")
        
        return new_posts

    async def check_for_new_posts_by_user(self, user_identifier: str) -> List[Dict[str, Any]]:
        """
        Check for new posts from a specific user since the last check time.
        
        Args:
            user_identifier (str): Either a Twitter user ID or screen name (handle without @)
            
        Returns:
            List[Dict[str, Any]]: A list of new posts found
        """
        new_posts = []
        current_time = datetime.now(timezone.utc)
        
        # If the identifier is not numeric, assume it's a screen name and get the user ID
        user_id = user_identifier
        if not user_identifier.isdigit():
            if user_identifier.startswith("@"):
                user_identifier = user_identifier[1:]
            # print("Try user ID first")
            user_id = await self.get_user_id(user_identifier)
            if not user_id:
                logger.error(f"Could not find user ID for screen name: {user_identifier}")
                return []
        
        if not self.timeline_route:
            raise ValueError("timeline_route is not initialized")
        
        try:
            endpoint = f"/graphql/UserTweets"
            variables = {
                "userId": user_id,
                "count": 20,
                "includePromotedContent": False,
                "withQuickPromoteEligibilityTweetFields": True,
                "withVoice": True,
                "withV2Timeline": True
            }
            features = {
                "responsive_web_graphql_exclude_directive_enabled": True,
                "verified_phone_label_enabled": False,
                "creator_subscriptions_tweet_preview_api_enabled": True,
                "responsive_web_graphql_timeline_navigation_enabled": True,
                "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                "c9s_tweet_anatomy_moderator_badge_enabled": True,
                "tweetypie_unmention_optimization_enabled": True,
                "responsive_web_edit_tweet_api_enabled": True,
                "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
                "view_counts_everywhere_api_enabled": True,
                "longform_notetweets_consumption_enabled": True,
                "responsive_web_twitter_article_tweet_consumption_enabled": False,
                "tweet_awards_web_tipping_enabled": False,
                "freedom_of_speech_not_reach_fetch_enabled": True,
                "standardized_nudges_misinfo": True,
                "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
                "rweb_video_timestamps_enabled": True,
                "longform_notetweets_rich_text_read_enabled": True,
                "longform_notetweets_inline_media_enabled": True,
                "responsive_web_enhance_cards_enabled": False,
                "rweb_tipjar_consumption_enabled": False,
                'creator_subscriptions_quote_tweet_preview_enabled': False,
                'articles_preview_enabled': False,
                'communities_web_enable_tweet_community_results_fetch': False,
                'rweb_lists_timeline_redesign_enabled': False,
                'responsive_web_media_download_video_enabled': False
                
            }
            
            params = {
                "variables": json.dumps(variables),
                "features": json.dumps(features)
            }
            
            params, headers = await self.authenticate_request("GET", endpoint, params, self.headers)
            response = await self._make_request(method="GET", endpoint=endpoint, params=params, headers=headers)
            if not response:
                logger.warning(f"Empty response for user {user_identifier}")
                return []
            
            if not isinstance(response, dict):
                logger.error(f"Unexpected response type for user {user_identifier}. Expected dict, got {type(response)}. Response: {response}")
                return []
                
            user_data = response.get('data', {}).get('user', {}).get('result', {})
            if not isinstance(user_data, dict):
                logger.error(f"Invalid user data format for user {user_identifier}. Got: {user_data}")
                return []
                
            timeline = user_data.get('timeline_v2', {}).get('timeline', {})
            if not isinstance(timeline, dict):
                logger.error(f"Invalid timeline format for user {user_identifier}. Got: {timeline}")
                return []
                
            instructions = timeline.get('instructions', [])
            for instruction in instructions:
                if instruction.get('type') == 'TimelineAddEntries':
                    entries = instruction.get('entries', [])
                    for entry in entries:
                        if entry.get('content', {}).get('entryType') == 'TimelineTimelineItem':
                            tweet = entry.get('content', {}).get('itemContent', {}).get('tweet_results', {}).get('result', {})
                            if tweet:
                                tweet_id = tweet.get('rest_id')
                                if tweet_id is None:
                                    continue
                                
                                legacy = tweet.get('legacy', {})
                                created_at = datetime.strptime(legacy.get('created_at', ''), '%a %b %d %H:%M:%S +0000 %Y').replace(tzinfo=timezone.utc)
                                
                                if created_at > self.last_check_time and tweet_id not in self.processed_tweets:
                                    self.processed_tweets.append(tweet_id)
                                    user = tweet.get('core', {}).get('user_results', {}).get('result', {}).get('legacy', {})
                                    
                                    # Get the tweet text and URLs
                                    text = legacy.get('full_text', '')
                                    urls = legacy.get('entities', {}).get('urls', [])
                                    
                                    # Replace shortened URLs with expanded ones
                                    for url in urls:
                                        short_url = url.get('url', '')
                                        expanded_url = url.get('expanded_url', '')
                                        if short_url and expanded_url:
                                            text = text.replace(short_url, expanded_url)
                                    
                                    new_post = {
                                        'id': tweet_id,
                                        'text': text,
                                        'user': user.get('screen_name'),
                                        'created_at': created_at
                                    }
                                    new_posts.append(new_post)
                                    logger.debug(f"New post added: {new_post}")
            
            self.last_check_time = current_time
            logger.info(f"Found {len(new_posts)} new posts from user {user_identifier}")
            return new_posts
            
        except Exception as e:
            logger.error(f"Error checking new posts for user {user_identifier}: {str(e)}")
            return []

    def _parse_search_results(self, data):
        # from pprint import pprint
        # pprint(data)
        search_results = []
        instructions = data.get('data', {}).get('search_by_raw_query', {}).get('search_timeline', {}).get('timeline', {}).get('instructions', [])
        
        for instruction in instructions:
            if instruction.get('type') == 'TimelineAddEntries':
                entries = instruction.get('entries', [])
                for entry in entries:
                    tweet = entry.get('content', {}).get('itemContent', {}).get('tweet_results', {}).get('result', {})
                    if tweet:
                        legacy = tweet.get('legacy', {})
                        user = tweet.get('core', {}).get('user_results', {}).get('result', {}).get('legacy', {})
                        entities = legacy.get('entities', {})
                        extended_entities = legacy.get('extended_entities', {})
                        
                        search_results.append({
                            'id': legacy.get('id_str'),
                            'full_text': legacy.get('full_text'),
                            'user': user.get('screen_name'),
                            'created_at': legacy.get('created_at'),
                            'handles': [f"@{mention['screen_name']}" for mention in entities.get('user_mentions', [])],
                            'websites': [url['expanded_url'] for url in entities.get('urls', [])],
                            'pic_links': [media['media_url_https'] for media in extended_entities.get('media', []) if media['type'] == 'photo']
                        })

        return search_results

    async def search_tweets(self, query: str, count: int = 40, cursor: str = "") -> Optional[Dict[str, Any]]:
        endpoint = "/graphql/SearchTimeline"
        variables = {
            "rawQuery": query,
            "count": count,
            "cursor": cursor,
            "querySource": "typed_query",
            "product": "Latest",
            "includePromotedContent": False
        }
        params = {
            "variables": json.dumps(variables)
        }
        
        try:
            print("Searching tweets...", query)
            params, headers = await self.authenticate_request("GET", endpoint, params, self.headers)
            data = await self._make_request(method="GET", endpoint=endpoint, params=params, headers=headers)
            return self._parse_search_results(data)
        except Exception as e:
            logger.error(f"Error searching tweets: {str(e)}")
            return None

    async def search_tweets_with_date_logic(self, handle: str, min_faves: int = 30) -> Optional[Dict[str, Any]]:
        since_date, until_date = self.get_date_range_for_search()
        query = f"from:{handle} min_faves:{min_faves} since:{since_date} until:{until_date}"
        return await self.search_tweets(query)

    async def search_tweets_from_user_with_keywords(self, handle: str, keywords: List[str], count: int = 40) -> Optional[Dict[str, Any]]:
        query = f"from:{handle}"
        if keywords:
            query += f" ({' OR '.join(keywords)})"
        return await self.search_tweets(query, count)

    async def get_user_id(self, screen_name: str) -> Optional[str]:
        if screen_name.startswith("@"):
            screen_name = screen_name[1:]
            
        if screen_name in self._user_id_cache:
            logger.debug(f"Cache hit for user {screen_name}")
            return self._user_id_cache[screen_name]
            
        endpoint = "/graphql/UserByScreenName"
        variables = {
            "screen_name": screen_name,
            "withSafetyModeUserFields": True,
            "withHighlightedLabel": True
        }
        features = {
            "hidden_profile_likes_enabled": True,
            "hidden_profile_subscriptions_enabled": True,
            "responsive_web_graphql_exclude_directive_enabled": True,
            "verified_phone_label_enabled": False,
            "subscriptions_verification_info_is_identity_verified_enabled": True,
            "subscriptions_verification_info_verified_since_enabled": True,
            "highlights_tweets_tab_ui_enabled": True,
            "creator_subscriptions_tweet_preview_api_enabled": True,
            "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
            "responsive_web_graphql_timeline_navigation_enabled": True,
            "creator_subscriptions_quote_tweet_preview_enabled": False,  # Required
            "articles_preview_enabled": True,  # Required
            "rweb_tipjar_consumption_enabled": True,  # Required
            "communities_web_enable_tweet_community_results_fetch": True  # Required
        }
        params = {
            "variables": json.dumps(variables),
            "features": json.dumps(features)
        }
        
        try:
            params, headers = await self.authenticate_request("GET", endpoint, params, self.headers)
            data = await self._make_request(method="GET", endpoint=endpoint, params=params, headers=headers)
            logger.debug(f"Raw response for user {screen_name}: {json.dumps(data, indent=2)}")
            
            if not data:
                logger.warning(f"Empty response when getting user ID for {screen_name}")
                return None
                
            if 'errors' in data:
                logger.warning(f"API errors for {screen_name}: {data['errors']}")
                return None
                
            user = data.get('data', {}).get('user', {}).get('result', {})
            if not user:
                logger.warning(f"User data not found in response for {screen_name}: {data}")
                return None
                
            user_id = user.get('rest_id')
            if user_id:
                logger.info(f"Found user ID {user_id} for {screen_name}")
                self._user_id_cache[screen_name] = user_id
                return user_id
            else:
                logger.warning(f"User ID not found in user data for {screen_name}: {user}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting user ID for {screen_name}: {str(e)}")
            return None

    async def get_tweet_by_rest_id(self, tweet_id: str) -> Optional[Dict[str, Any]]:
        endpoint = "/graphql/TweetResultByRestId"
        variables = {
            "tweetId": tweet_id,
            "withHighlightedLabel": True,
            "withTweetQuoteCount": True,
            "includePromotedContent": True,
            "withBirdwatchPivots": True,
            "withVoice": True,
            "withReactions": True
        }
        params = {"variables": json.dumps(variables)}
        
        try:
            params, headers = await self.authenticate_request("GET", endpoint, params, self.headers)
            data = await self._make_request(method="GET", endpoint=endpoint, params=params, headers=headers)
            tweet_result = data.get('data', {}).get('tweetResult', {}).get('result', {})

            print(f"Tweet result: {tweet_result}")
            if tweet_result and tweet_result.get('__typename') == 'Tweet':
                logger.info(f"Found tweet data for ID {tweet_id}")
                legacy = tweet_result.get('legacy', {})
                entities = legacy.get('entities', {})
                extended_entities = legacy.get('extended_entities', {})
                
                return {
                    'full_text': legacy.get('full_text', ''),
                    'handles': [f"@{mention['screen_name']}" for mention in entities.get('user_mentions', [])],
                    'websites': [url['expanded_url'] for url in entities.get('urls', [])],
                    'pic_links': [media['media_url_https'] for media in extended_entities.get('media', []) if media['type'] == 'photo']
                }
            else:
                logger.warning(f"Tweet data not found for ID {tweet_id}")
                return None
        except Exception as e:
            logger.error(f"Error getting tweet data for ID {tweet_id}: {str(e)}")
            return None

    async def get_user_tweets(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        endpoint = "/graphql/UserTweets"
        variables = {
            "userId": user_id,
            "count": limit,
            "includePromotedContent": True,
            "withBirdwatchPivots": True,
            "withVoice": True,
            "withReactions": True
        }
        params = {"variables": json.dumps(variables)}
        
        try:
            params, headers = await self.authenticate_request("GET", endpoint, params, self.headers)
            data = await self._make_request(method="GET", endpoint=endpoint, params=params, headers=headers)
            # print(f"Data: {data['data'][]}")
            instructions = data.get('data', {}).get('user', {}).get('result', {}).get('timeline', {}).get('timeline', {}).get('instructions', [])
            # print(f"Instructions: {instructions}")
            tweets = []
            for instruction in instructions:
                if instruction.get('type') == 'TimelineAddEntries':
                    entries = instruction.get('entries', [])
                    for entry in entries:
                        if entry.get('content', {}).get('entryType') == 'TimelineTimelineItem':
                            tweet_result = entry.get('content', {}).get('itemContent', {}).get('tweet_results', {}).get('result', {})
                            if tweet_result:
                                legacy = tweet_result.get('legacy', {})
                                tweets.append(legacy)
                                if len(tweets) >= limit:
                                    return tweets
            return tweets
        except Exception as e:
            logger.error(f"Error getting user tweets for ID {user_id}: {str(e)}")
            return []
    

    def get_date_range_for_search() -> tuple[str, str]:
        today = datetime.now().date()
        current_weekday = today.weekday()
        days_since_sunday = (current_weekday + 1) % 7
        most_recent_sunday = today - timedelta(days=days_since_sunday)
        
        if current_weekday < 2:
            since_date = most_recent_sunday - timedelta(days=7)
        else:
            since_date = most_recent_sunday
        
        return since_date.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d')

    async def get_list_members(self):
        """Get the current members of the monitored Twitter list."""
        if not self.list_route or not self.list_id:
            raise ValueError("list_route or list_id not initialized")
            
        endpoint = f"/graphql/{self.list_route}/ListMembers"
        variables = {
            "listId": self.list_id,
            "count": 100,  # Increased to get more members
            "withSafetyModeUserFields": True
        }
        features = {
            "rweb_tipjar_consumption_enabled": True,
            "responsive_web_graphql_exclude_directive_enabled": True,
            "verified_phone_label_enabled": False,
            "creator_subscriptions_tweet_preview_api_enabled": True,
            "responsive_web_graphql_timeline_navigation_enabled": True,
            "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
            "communities_web_enable_tweet_community_results_fetch": True,
            "c9s_tweet_anatomy_moderator_badge_enabled": True,
            "tweetypie_unmention_optimization_enabled": True,
            "responsive_web_edit_tweet_api_enabled": True,
            "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
            "view_counts_everywhere_api_enabled": True,
            "longform_notetweets_consumption_enabled": True,
            "responsive_web_twitter_article_tweet_consumption_enabled": True,
            "tweet_awards_web_tipping_enabled": False,
            "freedom_of_speech_not_reach_fetch_enabled": True,
            "standardized_nudges_misinfo": True,
            "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
            "rweb_video_timestamps_enabled": True,
            "longform_notetweets_rich_text_read_enabled": True,
            "longform_notetweets_inline_media_enabled": True,
            "responsive_web_enhance_cards_enabled": False,
            "articles_preview_enabled": True,
            "creator_subscriptions_quote_tweet_preview_enabled": False
        }
        params = {
            "variables": json.dumps(variables),
            "features": json.dumps(features)
        }
        
        try:
            params, headers = await self.authenticate_request("GET", endpoint, params, self.headers)
            data = await self._make_request(method="GET", endpoint=endpoint, params=params, headers=headers)
            if not data:
                logger.error("Failed to retrieve list members: Empty response")
                return []

            members = []
            instructions = data.get('data', {}).get('list', {}).get('members_timeline', {}).get('timeline', {}).get('instructions', [])
            
            for instruction in instructions:
                if instruction.get('type') == 'TimelineAddEntries':
                    entries = instruction.get('entries', [])
                    for entry in entries:
                        try:
                            if entry.get('content', {}).get('entryType') == 'TimelineTimelineItem':
                                user_results = entry.get('content', {}).get('itemContent', {}).get('user_results', {}).get('result', {})
                                if user_results:
                                    legacy = user_results.get('legacy', {})
                                    member = {
                                        'id': user_results.get('rest_id'),
                                        'screen_name': legacy.get('screen_name'),
                                        'name': legacy.get('name'),
                                        'description': legacy.get('description'),
                                        'followers_count': legacy.get('followers_count'),
                                        'following_count': legacy.get('friends_count'),
                                        'verified': legacy.get('verified', False),
                                        'profile_image_url': legacy.get('profile_image_url_https'),
                                        'created_at': legacy.get('created_at')
                                    }
                                    members.append(member)
                        except Exception as e:
                            logger.error(f"Error processing list member entry: {str(e)}")
                            continue

            logger.info(f"Retrieved {len(members)} list members")
            return members

        except Exception as e:
            logger.error(f"Error retrieving list members: {str(e)}")
            logger.exception("Exception details:")
            return []

    async def initialize_list_members(self):
        """Initialize the monitored accounts from the Twitter list."""
        if not self.list_route or not self.list_id:
            raise ValueError("list_route or list_id not initialized")
            
        endpoint = f"/graphql/{self.list_route}/ListMembers"
        variables = {
            "listId": self.list_id,
            "count": 100,  # Increased to get more members
            "withSafetyModeUserFields": True
        }
        features = {
            "rweb_tipjar_consumption_enabled": True,
            "responsive_web_graphql_exclude_directive_enabled": True,
            "verified_phone_label_enabled": False,
            "creator_subscriptions_tweet_preview_api_enabled": True,
            "responsive_web_graphql_timeline_navigation_enabled": True,
            "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
            "communities_web_enable_tweet_community_results_fetch": True,
            "c9s_tweet_anatomy_moderator_badge_enabled": True,
            "tweetypie_unmention_optimization_enabled": True,
            "responsive_web_edit_tweet_api_enabled": True,
            "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
            "view_counts_everywhere_api_enabled": True,
            "longform_notetweets_consumption_enabled": True,
            "responsive_web_twitter_article_tweet_consumption_enabled": True,
            "tweet_awards_web_tipping_enabled": False,
            "freedom_of_speech_not_reach_fetch_enabled": True,
            "standardized_nudges_misinfo": True,
            "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
            "rweb_video_timestamps_enabled": True,
            "longform_notetweets_rich_text_read_enabled": True,
            "longform_notetweets_inline_media_enabled": True,
            "responsive_web_enhance_cards_enabled": False,
            "articles_preview_enabled": True,
            "creator_subscriptions_quote_tweet_preview_enabled": False
        }
        params = {
            "variables": json.dumps(variables),
            "features": json.dumps(features)
        }
        
        try:
            params, headers = await self.authenticate_request("GET", endpoint, params, self.headers)
            data = await self._make_request(method="GET", endpoint=endpoint, params=params, headers=headers)
            if not data:
                logger.error("Failed to retrieve list members: Empty response")
                return

            # Clear existing monitored accounts before updating
            self.monitored_accounts.clear()
            
            instructions = data.get('data', {}).get('list', {}).get('members_timeline', {}).get('timeline', {}).get('instructions', [])
            for instruction in instructions:
                if instruction.get('type') == 'TimelineAddEntries':
                    entries = instruction.get('entries', [])
                    for entry in entries:
                        try:
                            if entry.get('content', {}).get('entryType') == 'TimelineTimelineItem':
                                user_results = entry.get('content', {}).get('itemContent', {}).get('user_results', {}).get('result', {})
                                if user_results:
                                    legacy = user_results.get('legacy', {})
                                    screen_name = legacy.get('screen_name')
                                    user_id = user_results.get('rest_id')
                                    if screen_name and user_id:
                                        self.monitored_accounts[screen_name] = user_id
                                        logger.debug(f"Added {screen_name}: {user_id} to monitored accounts")
                        except Exception as e:
                            logger.error(f"Error processing list member entry: {str(e)}")
                            continue

            logger.info(f"Initialized and updated {len(self.monitored_accounts)} monitored accounts from the list.")
        except Exception as e:
            logger.error(f"Error initializing list members: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())


    async def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user information by username."""
        endpoint = "/graphql/UserByScreenName"
        variables = {
            "screen_name": username,
            "withSafetyModeUserFields": True,
            "withHighlightedLabel": True
        }
        params = {
            "variables": json.dumps(variables)
        }
        
        try:
            params, headers = await self.authenticate_request("GET", endpoint, params, self.headers)
            data = await self._make_request(method="GET", endpoint=endpoint, params=params, headers=headers)
            user = data.get('data', {}).get('user', {}).get('result', {})
            if not user:
                logger.warning(f"User data not found for username {username}")
                return None
            return user
        except Exception as e:
            logger.error(f"Error getting user by username {username}: {str(e)}")
            return None
