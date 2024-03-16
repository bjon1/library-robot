// Serial Port Communication
import { SerialPort } from 'serialport'
const { ReadlineParser } = pkg;
import pkg from '@serialport/parser-readline'; // Import the parser module from the serialport package, for ES6 compatibility
const pathName = 'COM5'
const port = new SerialPort({ path: pathName, baudRate: 9600 })

// Create a parser to read lines from the serial port
const parser = port.pipe(new ReadlineParser({ delimiter: '\r\n' }))

// Read data from the serial port
parser.on("data", (line) => {
    console.log(line);
})

const States = {
    CRUISE: 1,
    FORWARD: 2,
    REVERSE: 3,
    TURNING_LEFT: 4,
    TURNING_RIGHT: 5,
    CLOCKWISE: 6,
    COUNTER_CLOCKWISE: 7,
    STOP: 8,
    STOP: 9
}

const moveForward = () => {
    console.log("Backend: RobotAPI.moveForward")
    port.write(States.CRUISE, (err) => {
        if (err) {
            return console.log('Error on write: ', err.message)
        }
        console.log('message written')
    })
    return true
}

const moveBackward = () => {
    console.log("Backend: RobotAPI.moveBackward")
    port.write(States.REVERSE, (err) => {
        if (err) {
            return console.log('Error on write: ', err.message)
        }
        console.log('message written')
    })
    return true
}

const turnLeft = () => {
    console.log("Backend: RobotAPI.turnLeft")
    port.write(States.TURNING_LEFT, (err) => {
        if (err) {
            return console.log('Error on write: ', err.message)
        }
        console.log('message written')
    })
    return true
}

const turnRight = () => {
    console.log("Backend: RobotAPI.turnRight")
    port.write(States.TURNING_RIGHT, (err) => {
        if (err) {
            return console.log('Error on write: ', err.message)
        }
        console.log('message written')
    })
    return true
}

const turnClockwise = () => {
    console.log("Backend: RobotAPI.turnClockwise")
    port.write(States.CLOCKWISE, (err) => {
        if (err) {
            return console.log('Error on write: ', err.message)
        }
        console.log('message written')
    })
    return true
}

const turnCounterClockwise = () => {
    console.log("Backend: RobotAPI.turnCounterClockwise")
    port.write(States.COUNTER_CLOCKWISE, (err) => {
        if (err) {
            return console.log('Error on write: ', err.message)
        }
        console.log('message written')
    })
    return true
}

const stopRobot = () => {
    console.log("Backend: RobotAPI.stopRobot")
    port.write(States.STOP, (err) => {
        if (err) {
            return console.log('Error on write: ', err.message)
        }
        console.log('message written')
    })
    return true
}

const setRobotSpeed = (speed) => {
    console.log("Backend: RobotAPI.setRobotSpeed")
    port.write(speed, (err) => {
        if (err) {
            return console.log('Error on write: ', err.message)
        }
        console.log('message written')
    })
    return true
}

const getRobotStatus = () => {
    console.log("Backend: RobotAPI.getRobotStatus")
    //implement the logic to get the robot status
}

export default {
    moveForward,
    moveBackward,
    turnLeft,
    turnRight,
    turnClockwise,
    turnCounterClockwise,
    stopRobot,
    setRobotSpeed,
    getRobotStatus
}
