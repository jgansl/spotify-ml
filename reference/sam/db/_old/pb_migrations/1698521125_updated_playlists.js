migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("w6zm9hujt26288n")

  collection.deleteRule = ""

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("w6zm9hujt26288n")

  collection.deleteRule = null

  return dao.saveCollection(collection)
})
