import logging
from datetime import datetime
import json


class NotesManager:
    def __init__(self):
        self.notes = []
        self.filename = "notes.json"

    def _generate_id(self):
        if not self.notes:
            return 1
        return max(note["id"] for note in self.notes) + 1

    def load_notes(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                self.notes = json.load(file)
        except FileNotFoundError:
            self.notes = []

    def save_notes(
        self,
    ):  # вызываю без параметров потому что буду использовать заметки и файл экземпляра класса
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(
                self.notes, file, ensure_ascii=False, indent=2
            )  # ensure_ascii=False, чтобы кириллица сохранялась читаемо, indent=2 для удобства чтения JSON.

    def _parse_tags(self, tags_str: str):
        if not tags_str:
            return []
        return [tag.strip() for tag in tags_str.split(",") if tag.strip()]

    def add_note(self, text: str, tags: str):
        if len(text) > 500:
            raise ValueError("Текст заметки не может быть длиннее 500 символов")

        created = (
            datetime.now().isoformat()
        )  # isoformat() даёт строку вида "2026-01-27T20:00:00", как в ТЗ.
        updated = created

        new_note = {
            "id": self._generate_id(),
            "text": text,
            "tags": self._parse_tags(tags),
            "created": created,
            "updated": updated,
        }
        self.notes.append(new_note)
        self.save_notes()

    def update_note(self, note_id: int, text: str, tags: str):
        if len(text) > 500:
            raise ValueError("Текст заметки не может быть длиннее 500 символов")
        updated = datetime.now().isoformat()
        for note in self.notes:
            if note["id"] == note_id:
                note["text"] = text
                note["tags"] = self._parse_tags(tags)
                note["updated"] = updated
                self.save_notes()
                return
        raise ValueError(f"Заметка с id={note_id} не найдена")

    def delete_note(self, note_id):
        for i, note in enumerate(self.notes):
            if note["id"] == note_id:
                del self.notes[i]
                self.save_notes()
                return

        raise ValueError(f"Заметка с id={note_id} не найдена")

    def search_notes(self, query: str) -> list[dict]:
        if not query.strip():
            return self.notes

        result = []
        for note in self.notes:
            if query.lower() in note["text"].lower() or query.lower() in [
                tag.lower() for tag in note["tags"]
            ]:
                result.append(note)
        return result
