/* 
    The package.json file is located in the root directory of the project. 
    Note that type: module is added to the package.json file to enable ES6 module syntax.
*/

import path, { dirname } from 'path'
import { fileURLToPath } from 'url'
import express from 'express'
import cors from 'cors'
import { SerialPort } from 'serialport'
import pkg from '@serialport/parser-readline'; // Import the parser module from the serialport package, for ES6 compatibility
const { ReadlineParser } = pkg;

const app = express()

// Middleware
app.use(express.json())
app.use(express.static(path.join(dirname(fileURLToPath(import.meta.url)), '../client/dist'))) // serve static files from the client side
app.use(cors({
    origin: 'http://localhost:3000', // origin of the request
    methods: 'GET,POST,PUT,DELETE,PATCH',
    credentials: true
}))

// Serial Port Communication

const pathName = 'COM5'
const port = new SerialPort({ path: pathName, baudRate: 9600 })

// Create a parser to read lines from the serial port
const parser = port.pipe(new ReadlineParser({ delimiter: '\r\n' }))

// Read data from the serial port
parser.on("data", (line) => {
    console.log(line);
})

// Write data to the serial port
port.write("ROBOT POWER ON\n", (err) => {
    if (err) {
        return console.log('Error on write: ', err.message)
    }
    console.log('message written')
})


// Add Controllers
import { robotController } from './controllers/robotController.js'
app.use('/api/robot', robotController)



app.get('*', (req, res) => { //catch all case for serving the static files, in case the user refreshes the page
    res.sendFile(path.join(dirname(fileURLToPath(import.meta.url)), '../client/dist/index.html'))
})


//Error Handling Middleware
app.use((err, req, res, next) => {
    console.error(err)
    const error_msg = {
        status: err.status || 500,
        message: err.message || 'Internal Server Error',
        isSuccess: false
    }
    res.status(error_msg.status).json(error_msg)
})

const PORT = process.env.PORT || 5000
app.listen(PORT, () => {
    console.log(`Server is running at http://localhost:${PORT}/`)
})