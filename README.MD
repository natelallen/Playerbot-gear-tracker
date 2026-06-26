# Playerbot‑Gear‑Tracker
Playerbot‑Gear‑Tracker is a lightweight Flask web application built to help track gear progression for **playerbots** on single‑player World of Warcraft servers (SPP, AzerothCore, etc.).

Managing gear needed for dozens of bots in spreadsheets quickly becomes unmanageable. This tool provides a clean, structured interface that lets you:
- Track accounts, **characters**, their **needed gear**, and the **dungeons** those items drop from  
- Add wishlist items per character
- Create preset gear templates (for those 20 warriors in your raid group)
- Dashboard summarizing:
  - Total drops needed per dungeon  
  - Total items needed per character  
  - Items grouped by dungeon → character → boss  
- Searchable dashboard (filter by dungeon, character, class, item)  
- Quickly see boss → item → character relationships  

## Data Notes / Known Issues
Currently, the item database supports **Vanilla WoW** only. The JSON dataset is incomplete and will expand over time as the app is used. However if you wanted to use this for other expansions of WoW you can add items individually, or find an item JSON database from another project and format it accordingly.

## How to Use

1. Add your **accounts**  
2. Add your **characters** and assign them to accounts  
3. Add items to each character’s **wishlist** (or assign a preset)
4. Use the **Dashboard** to see:
   - Which dungeons to farm  
   - Which characters need the most upgrades  
   - Which bosses drop the items you’re missing  
5. Modify or create **presets** for classes/specs as needed  

## Developer Notes

This project was created as a personal learning exercise.  
I’m not a professional developer — I’m learning Python and JavaScript as a Hobby.

The goals of this project were to:

- Get comfortable with **Flask Blueprints**  
- Improve my **Python** and **JavaScript**  
- Build something genuinely useful for my WoW single‑player setup  
- Learn how to structure a small web app end‑to‑end  

The code is functional but not “production‑grade.”  
I leaned heavily on AI assistance while debugging and implementing features.

This project uses:

- **Flask** (Python web framework)  
- **Jinja2** templates (HTML rendering)  
- **SQLite** database (`database.db`)  
- **Gunicorn** (optional, for production WSGI serving)  
- **Docker** (recommended deployment method)  

The app is intentionally lightweight and easy to self‑host.

## Installation

#### ⚠️ Security Warning
This project was **not** designed with hardened security practices in mind. It is intended for **local, private, self‑hosted environments only**. Do **NOT** expose this application directly to the public internet or a publicly accessable network.

### Docker Compose:


Create a simple `docker-compose.yml`:

```yaml
services:
  geartracker:
    image: ADDRESS/playerbot-gear-tracker:latest
    ports:
      - "5000:5000"
    volumes:
      - ./data:/app/data
    restart: unless-stopped
```

### Start the app:
docker compose up -d

### Access it at:
http://dockerhostip:5000

Optional: You can place this behind Traefik, Nginx Proxy Manager, Caddy, etc. If you already use a reverse-proxy on self hosted applications I will assume you know how to set that up. If for some reason other users have interest in using this application I might expand installation options / create a local executable version.

## License
This project is licensed under the MIT License.
See the LICENSE file for details.