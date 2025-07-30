
class RequestParsing:

    def __init__(self, request):
        self.application_instance = request

    @property
    def otps(self):
        if hasattr(self.application_instance, 'otps'):
            return self.application_instance.otps
        else:
            """update any other formats here"""

    @property
    def signatures(self):
        if hasattr(self.application_instance, 'signatures'):
            return self.application_instance.signatures
        if hasattr(self.application_instance, 'application_signatures'):
            return self.application_instance.application_signatures
        else:
            """update any other formats"""
            pass

    @property
    def node(self):
        return self.application_instance.node

    @property
    def save(self):
        return self.application_instance.save()


class ProcessedApplicationRequest(RequestParsing):

    def __init__(self, instance):
        super().__init__(instance)




