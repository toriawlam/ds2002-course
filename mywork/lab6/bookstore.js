// Task 2: use database
// use bookstore;

// Task 3: insert first author
// db.authors.insertOne({
//   "name": "Jane Austen",
//   "nationality": "British",
//   "bio": {
//     "short": "English novelist known for novels about the British landed gentry.",
//     "long": "Jane Austen was an English novelist whose works critique and comment upon the British landed gentry at the end of the 18th century. Her most famous novels include Pride and Prejudice, Sense and Sensibility, and Emma, celebrated for their wit, social commentary, and masterful character development."
//   }
// })

// Task 4: update to add birthday
// db.authors.updateOne({name:"Jane Austen"},{$set:{birthday:"1775-12-16"}})

// Task 5: insert four more authors
// db.authors.insertOne({
//     "name": 'Judy Blume',
//     "nationality": 'American',
//     "bio": {
//       "short": 'A renowned American author celebrated for her honest, candid, and often humorous literature for children, young adults, and adults',
//       "long": 'Judy Blum is an American author known for writing honest and candid literature for a wide range of audiences. Her work often explores themes of puberty, friendship, and family'
//     },
//     "birthday": '1938-2-12'
// })
// db.authors.insertOne({
//     "name": 'Roald Dahl',
//     "nationality": 'British',
//     "bio": {
//       "short": "Roald Dahl was a British author, poet, screenwriter, and fighter pilot who became famous for his children's books",
//       "long": "Roald Dahl is best known as a children's author for books like Charlie and the Chocolate Factory, Matilda, The BFG, and James and the Giant Peach. He is famous for quiry characters, magical tales, and a child's perspective"
//     },
//     "birthday": '1916-09-13'
// })
// db.authors.insertOne({
//     "name": 'Margaret Atwood',
//     "nationality": 'Canadian',
//     "bio": {
//       "short": 'Margaret Atwood is a prolific Canadian writer, poet, literary critic, and inventor who has published over 50 works across genres and media since the 1960s',
//       "long": "Margaret Atwood is best known for her speculative fiction novels, including The Handmaid's Tale, The Blind Assassin, and the MaddAddam trilogy. Her work is known for it's feminist perspective, and themes of survival, dystopia, and religion"
//     },
//     birthday: '1939-10-18'
// })
// db.authors.insertOne({
//     "name": 'George Orwell',
//     "nationality": 'British',
//     "bio": {
//       "short": 'George Orwell was a British author, novelist, and journalist',
//       "long": 'George Orwell was born in Bengal, India to British parents. Educated at Eton College in England, he served in the Indian Imperial Police in Burma before returning to Europe to write critically acclaimed works like Animal Farm and 1984'
//     },
//     "birthday": '1903-06-25'
// })

// Task 6: total count
// db.authors.countDocuments({})

// Task 7: British authors, sorted by name
// db.authors.find({nationality:"British"}).sort({name:1})