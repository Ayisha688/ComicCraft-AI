def build_comic_layout(panels, story):
    layout = []

    for i, panel in enumerate(panels):
        story_item = story[i] if isinstance(story, list) and i < len(story) else {}

        if not isinstance(story_item, dict):
            story_item = {}

        layout.append({
            "panel": panel.get("panel", i + 1),
            "title": panel.get("title", f"Panel {i + 1}"),
            "scene_description": panel.get("scene_description", ""),
            "image_prompt": panel.get("image_prompt", ""),
            "image_path": panel.get("image_path", ""),
            "narration": story_item.get("narration", ""),
            "dialogue": story_item.get("dialogue", ""),
            "caption": story_item.get("caption", ""),
        })

    return layout