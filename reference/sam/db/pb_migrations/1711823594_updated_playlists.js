migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("g2skj8b365ba8iq")

  collection.deleteRule = ""

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("g2skj8b365ba8iq")

  collection.deleteRule = null

  return dao.saveCollection(collection)
})
