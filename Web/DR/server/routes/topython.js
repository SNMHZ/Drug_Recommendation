const express = require('express')
const router = express.Router()
//const structjson = require('./structjson.js')

// Text Query Route
router.post('/textQuery', (req, res) => {
    
    text = req.body.text


    console.log(`text : ${text}`)
    res.send({text:text})
})

module.exports = router