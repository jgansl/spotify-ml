migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("6sdrnap1eiw7h2i")

  collection.deleteRule = ""

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("6sdrnap1eiw7h2i")

  collection.deleteRule = null

  return dao.saveCollection(collection)
})