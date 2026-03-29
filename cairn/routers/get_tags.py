from sqlalchemy.orm import Session
from cairn.models.entry import Tag

def _get_or_create_tag(db: Session, names: list[str]) -> list[Tag]:
    tags = []

    for name in names:
        tag = db.query(Tag).filter(Tag.name == name).first()
        if not tag:
            tag = Tag(name=name)
            db.add(tag)
        
        tags.append(tag)

    return tags