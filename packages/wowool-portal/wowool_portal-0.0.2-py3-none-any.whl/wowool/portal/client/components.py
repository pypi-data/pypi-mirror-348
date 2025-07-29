from wowool.portal.client.portal import Portal, _PortalMixin
from wowool.portal.client.error import ClientError
from wowool.portal.client.httpcode import HttpCode
from requests.exceptions import ReadTimeout
from dataclasses import dataclass


@dataclass
class Component:
    name: str
    type: str
    short_description: str | None = None


class Components(_PortalMixin):
    """
    :class:`Components` is a
    """

    def __init__(self, type: str = "", language: str = "", portal: Portal | None = None):
        super(Components, self).__init__(portal)
        if self.portal is None:
            # let try a default portal
            self.portal = Portal()

        assert (
            self.portal is not None
        ), "A Portal object must be provided, either directly by passing the 'portal' argument or by using the API through a context (with-statement)"
        self.type = type
        self.language = language
        self._components = self.get(type=type, language=language)

    def get(self, type: str = "", language: str = "", **kwargs):
        try:
            assert self.portal, "Portal not passed and not available from context"
            payload = self.portal._service.post(
                url="components",
                status_code=HttpCode.OK,
                data={
                    "apiKey": self.portal.api_key,
                    "language": language,
                    "type": type,
                },
                **kwargs,
            )

            if not payload:
                raise ClientError("Portal returned an invalid response")

            return [Component(**c) for c in payload]

        except ReadTimeout as ex:
            raise ClientError(str(ex))

    def __iter__(self):
        return iter(self._components)

    def __len__(self):
        return len(self._components)
