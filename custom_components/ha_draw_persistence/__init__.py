"""
Custom component for file upload in Home Assistant
Place this in your custom_components/ha_draw_persistence/ directory
"""
import json
import os
import logging
import voluptuous as vol
import aiofiles
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

    # Ensure upload directory exists
    os.makedirs(upload_directory, exist_ok=True)

    # Create a view for file uploads
    class JSONPersistenceView(HomeAssistantView):
        """Handle JSON persistence via Home Assistant API."""

        url = f'/api/ha_draw_persistence/upload'
        name = 'api:json_data_upload'
        requires_auth = True  # This ensures authentication is required

        async def post(self, request):
            """Handle JSON upload."""
            try:
                # Ensure proper authentication
                hass = request.app['hass']

                # Read multipart data
                data = await request.post()
                json_data = data.get("jsondata")
                file_name = data.get("filename")

                if not(file_name):
                    return self.json_message("No File Name Provided", status_code=400)

                if not json_data:
                    return self.json_message('No json send', status_code=400)

                try:
                    # Attempt to parse to ensure it's valid JSON
                    json.loads(json_data)
                except json.JSONDecodeError:
                    return self.json_message('Invalid JSON format', status_code=400)

                file_path = os.path.join(upload_directory, f"tldraw_persistence_{file_name}.json")

                # Save file
                async with aiofiles.open(file_path, 'w') as f:
                    await f.write(json_data)

                _LOGGER.info(f"successfully wrote Json Data: {json_data[:15]}")
                return self.json_message(f'Json Data {json_data[:15]} written successfully')

            except Exception as e:
                _LOGGER.error(f"Json Data error: {e}")
                return self.json_message('Upload failed', status_code=500)


        async def get(self, request):
            """Handle JSON retrieval."""
            hass = request.app['hass']

            try:
                file_name = request.query.get('filename', 'default')
                file_path = os.path.join(upload_directory, f"tldraw_persistence_{file_name}.json")

                # Check if file exists
                if not os.path.exists(file_path):
                    return self.json_message('No saved data', status_code=404)

                # Read file asynchronously
                async with aiofiles.open(file_path, 'r') as f:
                    json_data = await f.read()

                # Validate JSON before returning
                try:
                    json.loads(json_data)
                except json.JSONDecodeError:
                    return self.json_message('Stored data is not valid JSON', status_code=500)

                # Return JSON directly
                return self.json(json.loads(json_data))

            except Exception as e:
                _LOGGER.error(f"JSON Data read error: {e}", exc_info=True)
                return self.json_message('Retrieval failed', status_code=500)

    # Register the view
    hass.http.register_view(JSONPersistenceView())

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