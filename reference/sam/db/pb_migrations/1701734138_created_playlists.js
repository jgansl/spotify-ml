migrate((db) => {
  const collection = new Collection({
    "id": "g2skj8b365ba8iq",
    "created": "2023-12-04 23:55:38.031Z",
    "updated": "2023-12-04 23:55:38.031Z",
    "name": "playlists",
    "type": "base",
    "system": false,
    "schema": [
      {
        "system": false,
        "id": "mdyvauro",
        "name": "sid",
        "type": "text",
        "required": true,
        "unique": true,
        "options": {
          "min": null,
          "max": null,
          "pattern": ""
        }
      },
      {
        "system": false,
        "id": "iozz3n1b",
        "name": "spotify_id",
        "type": "text",
        "required": true,
        "unique": true,
        "options": {
          "min": null,
          "max": null,
          "pattern": ""
        }
      },
      {
        "system": false,
        "id": "s1qxnuit",
        "name": "name",
        "type": "text",
        "required": false,
        "unique": false,
        "options": {
          "min": null,
          "max": null,
          "pattern": ""
        }
      },
      {
        "system": false,
        "id": "cqrtopf1",
        "name": "follow",
        "type": "bool",
        "required": false,
        "unique": false,
        "options": {}
      }
    ],
    "listRule": null,
    "viewRule": null,
    "createRule": null,
    "updateRule": null,
    "deleteRule": null,
    "options": {}
  });

  return Dao(db).saveCollection(collection);
}, (db) => {
  const dao = new Dao(db);
  const collection = dao.findCollectionByNameOrId("g2skj8b365ba8iq");

  return dao.deleteCollection(collection);
})
