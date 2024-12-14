# HA-Draw-Persistence
## What does it do?
This is a simple Home Assistant integration that allows you to send the generated json data from the tldraw Canvas to Home Assistant and save it in a file.
It also allows you to load the saved json data from the file and display it on the tldraw Canvas.

## When do I need it?
If you want to use the Persistence feature of [ha-draw](https://github.com/JFK20/ha-draw-persistence).
So it's a direct dependency of [ha-draw](https://github.com/JFK20/ha-draw-persistence).

## How to install
1. Copy the Repository Url and add it as a custom repository in HACS.
2. Install the integration from HACS.
3. Add the following to your configuration.yaml file:
```yaml
ha_draw_persistence:
  name: ha_draw_persistence
  upload_directory: path/to/your/upload/directory
```
4. Restart Home Assistant.

The path to the upload directory is mandatory. The directory must be writable by Home Assistant.
You can for Example  use the following path: `/config/www/ha-draw-persistence/`