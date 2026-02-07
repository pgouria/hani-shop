from core.plugins.registry import registry

class ChannelMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # default channel
        channel_obj = None
        for channel in registry.channel:
            if channel.code == "website":
                channel_obj = channel
        request.channel = channel_obj
        return self.get_response(request)