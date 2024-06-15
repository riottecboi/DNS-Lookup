import validators


class DNS:
    def __init__(self, domain: str):
        self.domain = self.domain_validation(domain)

    async def domain_validation(self, domain):
        if validators.domain(domain):
            return domain
        else:
            return None
