import httpx
import typer
from datetime import datetime
from typing import Optional

app = typer.Typer(help="Cairn — personal data logger")
hikes_app = typer.Typer(help="Log and view hikes")
games_app = typer.Typer(help="Log and view games")
media_app = typer.Typer(help="Log and view media")
workouts_app = typer.Typer(help="Log and view workouts")
mood_app = typer.Typer(help="Log mood check-ins")

app.add_typer(hikes_app, name="hikes")
app.add_typer(games_app, name="games")
app.add_typer(media_app, name="media")
app.add_typer(workouts_app, name="workouts")
app.add_typer(mood_app, name="mood")

API_BASE = "http://127.0.0.1:8000"


# ---------------------------------------------------------------------------
# Hikes
# ---------------------------------------------------------------------------

@hikes_app.command("log")
def log_hike(
    trail: Optional[str] = typer.Option(None, "--trail", "-t", help="Trail name"),
    distance: Optional[float] = typer.Option(None, "--distance", "-d", help="Distance in km"),
    elevation: Optional[float] = typer.Option(None, "--elevation", "-e", help="Elevation gain in meters"),
    duration: Optional[int] = typer.Option(None, "--duration", help="Duration in minutes"),
    location: Optional[str] = typer.Option(None, "--location", "-l"),
    notes: Optional[str] = typer.Option(None, "--notes", "-n"),
    tags: Optional[str] = typer.Option(None, "--tags", help="Comma-separated tags"),
):
    """Log a hike."""
    payload = {
        "timestamp": datetime.now().isoformat(),
        "notes": notes,
        "tags": [t.strip() for t in tags.split(",")] if tags else [],
        "hike": {
            "trail_name": trail,
            "distance_km": distance,
            "elevation_gain_m": elevation,
            "duration_min": duration,
            "location": location,
        },
    }
    r = httpx.post(f"{API_BASE}/hikes/", json=payload)
    r.raise_for_status()
    typer.echo(f"Logged hike #{r.json()['id']}")


@hikes_app.command("list")
def list_hikes(
    tag: Optional[str] = typer.Option(None, "--tag"),
    limit: int = typer.Option(10, "--limit", "-n"),
):
    """List recent hikes."""
    params: dict = {"limit": limit}
    if tag:
        params["tag"] = tag
    r = httpx.get(f"{API_BASE}/hikes/", params=params)
    r.raise_for_status()
    for entry in r.json():
        hike = entry.get("hike", {})
        trail = hike.get("trail_name") or "unnamed"
        dist = hike.get("distance_km")
        dist_str = f"  {dist}km" if dist else ""
        ts = entry["timestamp"][:10]
        typer.echo(f"[{entry['id']}] {ts}  {trail}{dist_str}")


# ---------------------------------------------------------------------------
# Games, media, workouts, mood — TODO: implement following the hikes pattern
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Games
# ---------------------------------------------------------------------------

@games_app.command("log")
def log_game(
    title: Optional[str] = typer.Option(None, "--title", "-t", help="Game name"),
    platform: Optional[str] = typer.Option(None, "--platform", "-p", help="Platform game is played on"),
    status: Optional[str] = typer.Option(None, "--status", "-s", help="backlog/playing/complted/dropped"),
    hours: Optional[int] = typer.Option(None, "--hours", "-h", help="Hours invested in game"),
    rating: Optional[int] = typer.Option(None, "--rating", "-r"),
    notes: Optional[str] = typer.Option(None, "--notes", "-n"),
    tags: Optional[str] = typer.Option(None, "--tags", help="Comma-separated tags"),
):
    """Log a game."""
    payload = {
        "timestamp": datetime.now().isoformat(),
        "notes": notes,
        "tags": [t.strip() for t in tags.split(",")] if tags else [],
        "game": {
            "title": title,
            "platform": platform,
            "status": status,
            "hours": hours,
            "rating": rating,
        },
    }
    r = httpx.post(f"{API_BASE}/games/", json=payload)
    r.raise_for_status()
    typer.echo(f"Logged game #{r.json()['id']}")


@games_app.command("list")
def list_games(
    tag: Optional[str] = typer.Option(None, "--tag"),
    limit: int = typer.Option(10, "--limit", "-n"),
):
    """List recent games."""
    params: dict = {"limit": limit}
    if tag:
        params["tag"] = tag
    r = httpx.get(f"{API_BASE}/games/", params=params)
    r.raise_for_status()
    for entry in r.json():
        game = entry.get("game", {})
        title = game.get("title") or "unnamed"
        status = game.get("status")
        ts = entry["timestamp"][:10]
        typer.echo(f"[{entry['id']}] {ts}  {title} {status}")


if __name__ == "__main__":
    app()
