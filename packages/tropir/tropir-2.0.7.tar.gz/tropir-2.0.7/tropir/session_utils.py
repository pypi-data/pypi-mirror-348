import threading
import uuid
import os # Import os for environment variables
import logging # Import logging
import functools
from contextlib import contextmanager
import requests # Added for monkey-patching
import httpx # Added for httpx patching
from urllib.parse import urlparse # Added for URL parsing
import inspect # Added for checking async functions
import json # Added for JSON parsing and printing

# Define thread-local storage
_thread_local = threading.local()

# Global dictionary to store cross-thread sessions by name
# This will allow us to maintain session continuity between threads
_global_sessions_by_name = {}

# Global parent thread tracker
_parent_thread_sessions = {}

# Store original requests.Session.send method
_original_requests_session_send = requests.Session.send
_original_httpx_async_client_send = httpx.AsyncClient.send # Added for httpx

# Initialize thread-local storage
def _init_thread_local():
    if not hasattr(_thread_local, 'session_stack'):
        _thread_local.session_stack = []
    if not hasattr(_thread_local, 'named_sessions'):
        _thread_local.named_sessions = {}
    if not hasattr(_thread_local, 'session_id'):
        _thread_local.session_id = None
    if not hasattr(_thread_local, 'current_session_name'):
        _thread_local.current_session_name = None
    if not hasattr(_thread_local, 'patch_count'): # For requests
        _thread_local.patch_count = 0
    if not hasattr(_thread_local, 'httpx_patch_count'): # Added for httpx
        _thread_local.httpx_patch_count = 0

def _add_tropir_headers(headers_obj, url_str):
    """Helper function to add all Tropir headers to a headers object."""
    session_id = get_session_id()
    if session_id:
        headers_obj["X-Session-ID"] = str(session_id)
        logging.debug(f"Tropir Session: Added X-Session-ID to headers: {session_id}")
    else:
        logging.debug("Tropir Session: No active session ID found, X-Session-ID header not added.")

    session_name = get_session_name()
    if session_name:
        headers_obj["X-Session-Name"] = str(session_name)
        logging.debug(f"Tropir Session: Added X-Session-Name to headers: {session_name}")
    else:
        logging.debug("Tropir Session: No active session name found, X-Session-Name header not added.")

    tropir_api_key = os.environ.get("TROPIR_API_KEY")
    parsed_url = urlparse(url_str)
    hostname = parsed_url.hostname
    port = parsed_url.port

    target_host = False
    if (hostname == "api.tropir.com") or \
       (hostname == "localhost" and port == 8080) or \
       (hostname == "host.docker.internal" and port == 8080):
        target_host = True

    if tropir_api_key and target_host:
        headers_obj["X-TROPIR-API-KEY"] = tropir_api_key
        logging.debug("Tropir Session: Added X-TROPIR-API-KEY to headers for URL: %s", url_str)
    elif tropir_api_key:
        logging.debug("Tropir Session: TROPIR_API_KEY found, but URL %s does not match target hosts. Skipping header.", url_str)
    else:
        logging.debug("Tropir Session: TROPIR_API_KEY not found, skipping header.")
    
    return target_host # Return if it was a target host for logging body

def _log_request_details(url_str, headers_obj, body_content, content_type_str):
    """Helper function to log request details including headers and body."""
    print(f"--- Tropir Request to {url_str} ---")
    print("Headers:")
    # For httpx, headers can be a list of tuples or a dict. For requests, it's a dict.
    if isinstance(headers_obj, list): # httpx case
        for header_name, header_value in headers_obj:
            print(f"  {header_name}: {header_value}")
    elif isinstance(headers_obj, dict): # requests case
        for header_name, header_value in headers_obj.items():
            print(f"  {header_name}: {header_value}")
    
    print("Body:")
    if body_content:
        if "application/json" in content_type_str:
            try:
                body_data_to_log = body_content
                if isinstance(body_data_to_log, bytes):
                    body_data_to_log = body_data_to_log.decode('utf-8', errors='replace')
                json_body = json.loads(body_data_to_log)
                logging.debug(json.dumps(json_body, indent=2))
                print(json.dumps(json_body, indent=2))
            except (json.JSONDecodeError, UnicodeDecodeError) as e:
                logging.debug(f"Tropir Session: Could not parse JSON body: {e}. Raw body: {body_content}")
                print(f"(Non-JSON or Unparseable Body, Content-Type: {content_type_str})")
                print(body_content)
        else:
            logging.debug(f"Tropir Session: Body present but Content-Type is not application/json ({content_type_str}).")
            print(f"(Content-Type: {content_type_str})")
            if isinstance(body_content, bytes):
                try:
                    print(body_content.decode('utf-8', errors='replace'))
                except:
                    print(body_content) # Print as is if decode fails
            else:
                print(body_content)
    else:
        print("(No Body)")
    print("--- End Tropir Request ---")


async def _patched_httpx_async_client_send(client_instance, request, **kwargs):
    """
    Patched version of httpx.AsyncClient.send that adds Tropir session headers.
    """
    _add_tropir_headers(request.headers, str(request.url))
    
    content_type = request.headers.get("Content-Type", "").lower()
    # Check if it's a target host for detailed logging
    parsed_url = urlparse(str(request.url))
    hostname = parsed_url.hostname
    port = parsed_url.port
    is_target_host = (hostname == "api.tropir.com") or \
                     (hostname == "localhost" and port == 8080) or \
                     (hostname == "host.docker.internal" and port == 8080)

    if is_target_host:
        _log_request_details(str(request.url), request.headers, request.content, content_type)

    return await _original_httpx_async_client_send(client_instance, request, **kwargs)


def _patched_requests_session_send(session_instance, request, **kwargs):
    """
    Patched version of requests.Session.send that adds Tropir session headers.
    """
    is_target_host = _add_tropir_headers(request.headers, request.url)
    
    if is_target_host:
        content_type = request.headers.get("Content-Type", "").lower()
        _log_request_details(request.url, request.headers, request.body, content_type)

    return _original_requests_session_send(session_instance, request, **kwargs)

def _apply_requests_patch_if_needed():
    _init_thread_local() 
    if _thread_local.patch_count == 0:
        requests.Session.send = _patched_requests_session_send
        logging.debug("Tropir Session: Patched requests.Session.send.")
    _thread_local.patch_count += 1

def _revert_requests_patch_if_needed():
    _init_thread_local() 
    if hasattr(_thread_local, 'patch_count') and _thread_local.patch_count > 0:
        _thread_local.patch_count -= 1
        if _thread_local.patch_count == 0:
            requests.Session.send = _original_requests_session_send
            logging.debug("Tropir Session: Reverted requests.Session.send to original.")
    elif hasattr(_thread_local, 'patch_count') and _thread_local.patch_count == 0 :
        if requests.Session.send != _original_requests_session_send:
             requests.Session.send = _original_requests_session_send
             logging.warning("Tropir Session: patch_count (requests) was 0 but send was not original. Reverted.")

def _apply_httpx_patch_if_needed():
    _init_thread_local()
    if _thread_local.httpx_patch_count == 0:
        httpx.AsyncClient.send = _patched_httpx_async_client_send
        logging.debug("Tropir Session: Patched httpx.AsyncClient.send.")
    _thread_local.httpx_patch_count += 1

def _revert_httpx_patch_if_needed():
    _init_thread_local()
    if hasattr(_thread_local, 'httpx_patch_count') and _thread_local.httpx_patch_count > 0:
        _thread_local.httpx_patch_count -= 1
        if _thread_local.httpx_patch_count == 0:
            httpx.AsyncClient.send = _original_httpx_async_client_send
            logging.debug("Tropir Session: Reverted httpx.AsyncClient.send to original.")
    elif hasattr(_thread_local, 'httpx_patch_count') and _thread_local.httpx_patch_count == 0:
        if httpx.AsyncClient.send != _original_httpx_async_client_send:
            httpx.AsyncClient.send = _original_httpx_async_client_send
            logging.warning("Tropir Session: httpx_patch_count was 0 but send was not original. Reverted.")

def _inherit_parent_session():
    """Inherit session from parent thread if available."""
    current_thread = threading.current_thread()
    
    # Skip for MainThread since it has no parent
    if current_thread.name == 'MainThread':
        return
    
    # Check if there's a parent session we can inherit
    if 'MainThread' in _parent_thread_sessions:
        parent_session = _parent_thread_sessions['MainThread']
        if parent_session:
            session_id, session_name = parent_session
            set_session_id(session_id, session_name)
            logging.debug(f"Thread {current_thread.name} inherited session {session_name} ({session_id}) from MainThread")

def get_session_id():
    """Get the current session ID.
    
    First checks thread-local storage, then tries to inherit from parent thread if needed.
    
    Returns:
        str or None: The current session ID if one exists, otherwise None.
    """
    _init_thread_local()
    
    # Check thread-local stack first
    if _thread_local.session_stack:
        return _thread_local.session_stack[-1]
    
    # Then check thread-local session ID
    if _thread_local.session_id:
        return _thread_local.session_id
    
    # Try to inherit from parent if we don't have a session yet
    _inherit_parent_session()
    
    # Check again after potential inheritance
    if _thread_local.session_stack:
        return _thread_local.session_stack[-1]
    if _thread_local.session_id:
        return _thread_local.session_id
    
    # No session found
    return None

def get_session_name():
    """Get the current session name, if any."""
    _init_thread_local()
    
    # Try to inherit from parent if we don't have a session yet
    if not hasattr(_thread_local, 'current_session_name') or not _thread_local.current_session_name:
        _inherit_parent_session()
        
    return getattr(_thread_local, 'current_session_name', None)

def set_session_id(session_id, session_name=None):
    """Set the session ID for the current thread.
    
    Also registers the session ID globally for cross-thread usage.
    
    Args:
        session_id: The session ID to set
        session_name: Optional name to associate with this session
    """
    _init_thread_local()
    _thread_local.session_id = session_id
    
    # Register in global sessions for inheritance by child threads
    current_thread = threading.current_thread().name
    _parent_thread_sessions[current_thread] = (session_id, session_name)
    
    if session_name:
        _thread_local.current_session_name = session_name
        if not hasattr(_thread_local, 'named_sessions'):
            _thread_local.named_sessions = {}
        _thread_local.named_sessions[session_name] = session_id
        
        # Store in global sessions by name
        _global_sessions_by_name[session_name] = session_id

def clear_session_id():
    """Clear the session ID for the current thread."""
    _init_thread_local()
    _thread_local.session_id = None
    _thread_local.session_stack = []
    
    # Don't clear named sessions dictionary - we want persistence
    # But do clear current session name
    _thread_local.current_session_name = None
    
    # Remove from parent thread register
    current_thread = threading.current_thread().name
    if current_thread in _parent_thread_sessions:
        del _parent_thread_sessions[current_thread]

@contextmanager
def session(session_name=None):
    """Context manager for defining session boundaries.
    
    Args:
        session_name: Optional name for the session. If provided and this
                     session has been used before, the same session ID will be reused.
    """
    _init_thread_local()
    previous_stack = list(_thread_local.session_stack)  # Create a copy of the stack
    previous_session_name = _thread_local.current_session_name
    
    # Generate or retrieve session ID
    # First check thread-local named sessions
    if session_name and session_name in _thread_local.named_sessions:
        session_id = _thread_local.named_sessions[session_name]
    # Then check global sessions by name
    elif session_name and session_name in _global_sessions_by_name:
        session_id = _global_sessions_by_name[session_name]
        # Copy to thread-local too
        _thread_local.named_sessions[session_name] = session_id
    else:
        session_id = str(uuid.uuid4())
        if session_name:
            _thread_local.named_sessions[session_name] = session_id
            _global_sessions_by_name[session_name] = session_id
    
    # Push session ID to the stack and set current session name
    _thread_local.session_stack.append(session_id)
    _thread_local.current_session_name = session_name
    
    # Register in parent thread sessions for inheritance by child threads
    current_thread = threading.current_thread().name
    _parent_thread_sessions[current_thread] = (session_id, session_name)
    
    _apply_requests_patch_if_needed() # Apply requests patch
    _apply_httpx_patch_if_needed() # Apply httpx patch
    logging.debug(f"Started session: {session_name or 'unnamed'} with ID: {session_id} on thread {current_thread}")
    
    try:
        yield session_id
    finally:
        # Restore previous stack state and session name
        _thread_local.session_stack = previous_stack
        _thread_local.current_session_name = previous_session_name
        
        # Update parent thread sessions register with previous state
        if previous_session_name:
            prev_id = _thread_local.named_sessions.get(previous_session_name)
            if prev_id:
                _parent_thread_sessions[current_thread] = (prev_id, previous_session_name)
        elif not previous_stack and not previous_session_name:
            # If we're ending all sessions, remove from parent thread register
            if current_thread in _parent_thread_sessions:
                del _parent_thread_sessions[current_thread]
        
        _revert_requests_patch_if_needed() # Revert requests patch
        _revert_httpx_patch_if_needed() # Revert httpx patch
        logging.debug(f"Ended session: {session_name or 'unnamed'} on thread {current_thread}")

def begin_session(session_name_or_func=None):
    """Decorator or function to begin a session.
    
    This can be used as a decorator around a function or as a function call
    to mark the beginning of a session.
    
    Args:
        session_name_or_func: Optional name for the session, or the function to decorate.
                             If a name is provided and this session has been used before,
                             the same session ID will be reused. If used as @begin_session
                             with no arguments, the function name is used as the session name.
    """
    _init_thread_local()

    param = session_name_or_func

    # Case 1: Used as @begin_session (param is the function to decorate)
    if callable(param) and not isinstance(param, functools.partial): # Make sure it's a function/method not a partial
        func_to_decorate = param
        session_name_to_use = getattr(func_to_decorate, '__name__', 'unnamed_session')

        if inspect.iscoroutinefunction(func_to_decorate):
            @functools.wraps(func_to_decorate)
            async def async_wrapper(*args, **kwargs):
                with session(session_name_to_use):
                    return await func_to_decorate(*args, **kwargs)
            return async_wrapper
        else:
            @functools.wraps(func_to_decorate)
            def sync_wrapper(*args, **kwargs):
                with session(session_name_to_use):
                    return func_to_decorate(*args, **kwargs)
            return sync_wrapper

    # Case 2: Used as @begin_session("name") or @begin_session() which returns a decorator,
    # or as a direct call: begin_session("name")
    # Here, param is the session name (a string) or None.
    else:
        session_name_from_call = param  # This is the name passed like begin_session("my_name"), or None

        def decorator_factory(func_to_decorate):
            # If @begin_session() was used, session_name_from_call is None; use func_to_decorate name.
            # If @begin_session("my_name") was used, session_name_from_call is "my_name".
            actual_session_name = session_name_from_call if session_name_from_call is not None \
                                else getattr(func_to_decorate, '__name__', 'unnamed_session')

            if inspect.iscoroutinefunction(func_to_decorate):
                @functools.wraps(func_to_decorate)
                async def async_wrapper(*args, **kwargs):
                    with session(actual_session_name):
                        return await func_to_decorate(*args, **kwargs)
                return async_wrapper
            else:
                @functools.wraps(func_to_decorate)
                def sync_wrapper(*args, **kwargs):
                    with session(actual_session_name):
                        return func_to_decorate(*args, **kwargs)
                return sync_wrapper
        
        # If begin_session("some_name") was called directly, this part also starts the session.
        if isinstance(session_name_from_call, str):
            # Logic to immediately start a session if begin_session("name") is called directly.
            # This is copied and adapted from the original function's behavior.
            
            # Ensure _thread_local attributes exist if not already (though _init_thread_local should handle it)
            if not hasattr(_thread_local, 'named_sessions'): _thread_local.named_sessions = {}
            if not hasattr(_thread_local, 'session_stack'): _thread_local.session_stack = []

            session_id_to_start = None
            if session_name_from_call in _thread_local.named_sessions:
                session_id_to_start = _thread_local.named_sessions[session_name_from_call]
            elif session_name_from_call in _global_sessions_by_name:
                session_id_to_start = _global_sessions_by_name[session_name_from_call]
                _thread_local.named_sessions[session_name_from_call] = session_id_to_start # copy to thread-local
            else:
                session_id_to_start = str(uuid.uuid4())
                _thread_local.named_sessions[session_name_from_call] = session_id_to_start
                _global_sessions_by_name[session_name_from_call] = session_id_to_start
            
            _thread_local.session_stack.append(session_id_to_start)
            _thread_local.current_session_name = session_name_from_call
            
            current_thread_name = threading.current_thread().name
            _parent_thread_sessions[current_thread_name] = (session_id_to_start, session_name_from_call)
            
            _apply_requests_patch_if_needed()
            _apply_httpx_patch_if_needed() # Apply httpx patch
            logging.debug(f"Started session: {session_name_from_call} with ID: {session_id_to_start} on thread {current_thread_name} (via direct begin_session call)")

        return decorator_factory

def end_session(session_name=None):
    """Function to end a session.
    
    Args:
        session_name: Optional name of the session to end. If not provided,
                     the most recent session will be ended.
    """
    _init_thread_local()
    
    current_thread = threading.current_thread().name
    
    if _thread_local.session_stack:
        session_id = _thread_local.session_stack.pop()
        # Clear current session name if it matches the ended session
        if _thread_local.current_session_name == session_name:
            _thread_local.current_session_name = None
            # Remove from parent thread sessions if no more sessions
            if not _thread_local.session_stack:
                if current_thread in _parent_thread_sessions:
                    del _parent_thread_sessions[current_thread]
        
        _revert_requests_patch_if_needed() # Revert requests patch
        _revert_httpx_patch_if_needed() # Revert httpx patch
        logging.debug(f"Ended session: {session_name or 'unnamed'} with ID: {session_id} on thread {current_thread}")
    else:
        logging.warning(f"Attempted to end session {session_name or 'unnamed'} but no active sessions found on thread {current_thread}")

# Monkey-patch threading.Thread to enable automatic session inheritance
_original_thread_init = threading.Thread.__init__

def _thread_init_with_session_inheritance(self, *args, **kwargs):
    # Call the original __init__
    _original_thread_init(self, *args, **kwargs)
    
    # Store the current thread's session info for inheritance
    if threading.current_thread().name in _parent_thread_sessions:
        self._parent_session = _parent_thread_sessions[threading.current_thread().name]
    else:
        self._parent_session = None

threading.Thread.__init__ = _thread_init_with_session_inheritance

# Monkey-patch threading.Thread.run to inherit session on start
_original_thread_run = threading.Thread.run

def _thread_run_with_session_inheritance(self):
    # Set up session inheritance if we have parent session info
    if hasattr(self, '_parent_session') and self._parent_session:
        session_id, session_name = self._parent_session
        if session_id and session_name:
            set_session_id(session_id, session_name)
            logging.debug(f"Thread {self.name} inherited session {session_name} ({session_id})")
    
    # Call the original run method
    _original_thread_run(self)

threading.Thread.run = _thread_run_with_session_inheritance 