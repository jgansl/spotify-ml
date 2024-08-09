migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("yguxfq91ip5me0u")

  collection.listRule = ""
  collection.viewRule = ""

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("yguxfq91ip5me0u")

  collection.listRule = null
  collection.viewRule = null

  return dao.saveCollection(collection)
})
