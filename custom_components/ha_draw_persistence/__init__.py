"""
Custom component for file upload in Home Assistant
Place this in your custom_components/ha_draw_persistence/ directory
"""
import os
import logging
import voluptuous as vol
import aiofiles
import uuid
import homeassistant.helpers.config_validation as cv
from homeassistant.components.http import HomeAssistantView
from homeassistant.const import CONF_NAME
from homeassistant.config_entries import ConfigFlow, ConfigEntry
from homeassistant.core import HomeAssistant

DOMAIN = "ha_draw_persistence"
_LOGGER = logging.getLogger(__name__)

# Configuration schema
CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_NAME): cv.string,
        vol.Required('upload_directory'): cv.string,
        vol.Optional('allowed_extensions', default=['json']): vol.All(cv.ensure_list, [cv.string])
    })
}, extra=vol.ALLOW_EXTRA)


async def async_setup(hass, config):
    """Set up the file upload component."""
    conf = config.get(DOMAIN, {})
    upload_directory = conf.get('upload_directory')
    name = conf.get(CONF_NAME, 'File Upload')
    allowed_extensions = conf.get('allowed_extensions', ['json'])

    # Ensure upload directory exists
    os.makedirs(upload_directory, exist_ok=True)

    # Create a view for file uploads
    class FileUploadView(HomeAssistantView):
        """Handle file uploads via Home Assistant API."""

        url = f'/api/{DOMAIN}/upload'
        name = 'api:file_upload'
        requires_auth = True  # This ensures authentication is required

        async def post(self, request):
            """Handle file upload."""
            try:
                # Ensure proper authentication
                hass = request.app['hass']

                # Read multipart data
                data = await request.post()
                uploaded_file = data.get('file')

                if not uploaded_file:
                    return self.json_message('No file uploaded', status_code=400)

                # Check file extension
                file_ext = uploaded_file.filename.split('.')[-1].lower()
                if file_ext not in allowed_extensions:
                    return self.json_message(f'File type not allowed. Allowed: {allowed_extensions}', status_code=400)

                # Generate unique filename
                unique_filename = f"{uuid.uuid4()}_{uploaded_file.filename}"
                file_path = os.path.join(upload_directory, unique_filename)

                # Save file
                async with aiofiles.open(file_path, 'wb') as f:
                    await f.write(uploaded_file.file.read())

                _LOGGER.info(f"File uploaded successfully: {unique_filename}")
                return self.json_message(f'File {unique_filename} uploaded successfully')

            except Exception as e:
                _LOGGER.error(f"File upload error: {e}")
                return self.json_message('Upload failed', status_code=500)

    # Register the view
    hass.http.register_view(FileUploadView())

    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up from a config entry."""
    # This is required for config flow support
    return True

class HADrawPersistenceConfigFlow(ConfigFlow, domain=DOMAIN):
    """Config flow for ha_draw_persistence."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        # This is a placeholder. You might want to add more configuration options.
        return self.async_create_entry(title=DOMAIN, data={})