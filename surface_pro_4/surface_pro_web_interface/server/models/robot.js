// Serial portSender Communication
import { SerialPort, ReadlineParser } from 'serialport'


const portSender = new SerialPort({
    baudRate: 9600,
    path: 'COM5'
})

const portReceiver = new SerialPort({
    baudRate: 9600,
    path: 'COM6'
})

setTimeout(() => {
    portSender.write('test', (err) => {
        if (err) {
            return console.log('Error on write: ', err.message)
        }
        console.log('message written')
    })
}, 3000);



const parser = portReceiver.pipe(new ReadlineParser({ delimiter: '\r\n' }))

let accumulatedData = '';

portReceiver.on('data', (data) => {
    accumulatedData += data.toString();
});

setInterval(() => {
    if (accumulatedData !== '') {
        console.log('Data:', parseInt(accumulatedData, 10));
        accumulatedData = '';
    }
}, 100);


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
    portSender.write(Buffer.from([States.CRUISE]), (err) => {
        if (err) {
            return console.log('Error on write: ', err.message)
        }
        console.log('message written')
    })
    return true
}

const moveBackward = () => {
    console.log("Backend: RobotAPI.moveBackward")
    portSender.write(Buffer.from([States.REVERSE]), (err) => {
        if (err) {
            return console.log('Error on write: ', err.message)
        }
        console.log('message written')
    })
    return true
}

const turnLeft = () => {
    console.log("Backend: RobotAPI.turnLeft")
    portSender.write(Buffer.from([States.TURNING_LEFT]), (err) => {
        if (err) {
            return console.log('Error on write: ', err.message)
        }
        console.log('message written')
    })
    return true
}

const turnRight = () => {
    console.log("Backend: RobotAPI.turnRight")
    portSender.write(Buffer.from([States.TURNING_RIGHT]), (err) => {
        if (err) {
            return console.log('Error on write: ', err.message)
        }
        console.log('message written')
    })
    return true
}

const turnClockwise = () => {
    console.log("Backend: RobotAPI.turnClockwise")
    portSender.write(Buffer.from([States.CLOCKWISE]), (err) => {
        if (err) {
            return console.log('Error on write: ', err.message)
        }
        console.log('message written')
    })
    return true
}

const turnCounterClockwise = () => {
    console.log("Backend: RobotAPI.turnCounterClockwise")
    portSender.write(Buffer.from([States.COUNTER_CLOCKWISE]), (err) => {
        if (err) {
            return console.log('Error on write: ', err.message)
        }
        console.log('message written')
    })
    return true
}

const stopRobot = () => {
    console.log("Backend: RobotAPI.stopRobot")
    portSender.write(Buffer.from([States.STOP]), (err) => {
        if (err) {
            return console.log('Error on write: ', err.message)
        }
        console.log('message written')
    })
    return true
}

const setRobotSpeed = (speed) => {
    console.log("Backend: RobotAPI.setRobotSpeed")
    portSender.write(Buffer.from([speed]), (err) => {
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
