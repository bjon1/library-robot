import net from 'net'

const port = 50000;
const host = '137.140.212.230'

const client = new net.Socket();

const connectToServer = () => {
    client.connect(port, host, () => {
        console.log('Connected to server');
    });
}

const closeConnection = () => {
    client.end(() => {
        console.log('Connection closed by client');
    });
}

connectToServer(); // initial connection

client.on('data', (data) => {
    console.log('Received: ' + data);
})

client.on('error', (error) => {
    console.log('Error, Connection closed');
    throw new Error('Error, Connection closed');    
});

client.on('close', () => {
    console.log('Connection closed');
    throw new Error('Connection closed');
});

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
    const buffer = new Uint8Array([States.FORWARD]);
    client.write(buffer);
    return "Sent " + States.FORWARD;
}

const moveBackward = () => {
    console.log('moveBackward')
    const buffer = new Uint8Array([States.REVERSE]);
    client.write(buffer);
    return "Sent " + States.REVERSE;
}

const turnLeft = () => {
    console.log('turnLeft')
    const buffer = new Uint8Array([States.TURNING_LEFT]);
    client.write(buffer);
    return "Sent " + States.TURNING_LEFT;
}

const turnRight = () => {
    console.log('turnRight')
    const buffer = new Uint8Array([States.TURNING_RIGHT]);
    client.write(buffer);
    return "Sent " + States.TURNING_RIGHT;
}

const turnClockwise = () => {
    console.log('turnClockwise')
    const buffer = new Uint8Array([States.CLOCKWISE]);
    client.write(buffer);
    return "Sent " + States.CLOCKWISE;
}

const turnCounterClockwise = () => {
    console.log('turnCounterClockwise')
    const buffer = new Uint8Array([States.COUNTER_CLOCKWISE]);
    client.write(buffer);
    return "Sent " + States.COUNTER_CLOCKWISE;
}

const setRobotSpeed = (speed) => {
    console.log('setRobotSpeed')
    const buffer = new Uint8Array([speed]);
    client.write(buffer);
    return "Sent " + speed;
}

const stopRobot = () => {
    console.log('stopRobot')
    const buffer = new Uint8Array([States.STOP]);
    client.write(buffer);
    return "Sent " + States.STOP;
}

export default {
    moveForward,
    moveBackward,
    turnLeft,
    turnRight,
    turnClockwise,
    turnCounterClockwise,
    stopRobot,
    setRobotSpeed
}
