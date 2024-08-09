migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("a75cw1kbc9cxewc")

  collection.deleteRule = ""

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("a75cw1kbc9cxewc")

  collection.deleteRule = null

  return dao.saveCollection(collection)
})
