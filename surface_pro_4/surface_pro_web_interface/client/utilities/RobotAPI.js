import { request } from './API.js'

    /* Endpoints:
    *  - /api/robot/move-forward
    *  - /api/robot/move-backward
    *  - /api/robot/turn-left
    *  - /api/robot/turn-right
    *  - /api/robot/turn-clockwise
    *  - /api/robot/turn-counter-clockwise
    *  - /api/robot/stop-robot
    *  - /api/robot/status
    */


const moveForward = () => {
    console.log('RobotAPI.moveForward');
    const response = request('POST', '/api/robot/move-forward')
    return response
}

const moveBackward = () => {
    console.log('RobotAPI.moveBackward');
    const response = request('POST', '/api/robot/move-backward')
    return response
}

const turnLeft = () => {
    console.log('RobotAPI.turnLeft');
    const response = request('POST', '/api/robot/turn-left')
    return response
}

const turnRight = () => {
    console.log('RobotAPI.turnRight');
    const response = request('POST', '/api/robot/turn-right')
    return response
}

const turnClockwise = () => {
    console.log('RobotAPI.turnClockwise');
    const response = request('POST', '/api/robot/turn-clockwise')
    return response
}

const turnCounterClockwise = () => {
    console.log('RobotAPI.turnCounterClockwise');
    const response = request('POST', '/api/robot/turn-counter-clockwise')
    return response
}

const stopRobot = () => {
    console.log('RobotAPI.stopRobot');
    const response = request('POST', '/api/robot/stop-robot') 
    return response     
}

const setRobotSpeed = (speed) => {
    console.log('RobotAPI.setRobotSpeed');
    const response = request('POST', '/api/robot/set-speed', { speed })
    return response
}

const getRobotStatus = async () => {
    console.log('RobotAPI.getRobotStatus');
    const response = await request('GET', '/api/robot/status')
    return response
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
