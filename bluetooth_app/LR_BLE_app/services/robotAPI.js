

const cruise = () => {
    alert("Cruising")
}

const goForward = () => {
    alert("Going Forward")
}

const reverse = () => {
    alert("Reversing")
}

const turnLeft = () => {
    alert("Turning Left")
}

const turnRight = () => {
    alert("Turning Right")
}

const stop = () => {
    alert("Stopping")
}

const sendCommand = (command) => {
    alert("Sending Command: " + command)
}


export default {
    cruise,
    goForward,
    reverse,
    turnLeft,
    turnRight,
    stop,
    sendCommand
}