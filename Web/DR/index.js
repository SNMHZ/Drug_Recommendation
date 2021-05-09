const express = require("express")
const bodyParser = require("body-parser")
const app = express()

app.use(bodyParser.urlencoded({extended: true}))
app.use(bodyParser.json())

app.use('/api/topython', require('./server/routes/topython'))

if (process.env.NODE_ENV == "production") {
    app.use(express.static("client/build"))

    app.get("*", (req, res) => {
        res.sendFile(path.resolve(__dirname, "client", "build", "index.html"))
    })
}

const port = 5000

app.listen(port, () => {
    console.log(`Server Running at ${port}`)
})