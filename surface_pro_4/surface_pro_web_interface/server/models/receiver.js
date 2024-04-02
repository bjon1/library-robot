const SerialPort = require('serialport');
const Readline = require('@serialport/parser-readline');

const port = new SerialPort('COM6', { baudRate: 9600 });

const parser = port.pipe(new Readline());

parser.on('data', (line) => {
  console.log(line);
});