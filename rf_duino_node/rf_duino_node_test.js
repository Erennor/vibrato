var RFDuino = require('./index.js');
var debug = require('debug')('rf_duino_node_test');
var async = require('async');

/************************************************
 * rf_duino_node_test.js
 * test rf duino node
 *************************************************/

//object to test
var rfDuino = null;

/**************************************
 * Exit handlers
 ***************************************/
function cleanRFDuino() {
	debug('clean test');
	if (rfDuino !== null) {
		rfDuino.disconnect();
		rfDuino = null;
	}
	debug('rf_duino_node_test : TEST END');
}

function exitHandler(options, err) {
	if (options.cleanup) {cleanRFDuino();}
	if (err) {debug(err.stack);}
	if (options.exit) {process.exit();}
}

//do something when app is closing
process.on('exit', exitHandler.bind(null, {
	cleanup: true
}));

//catches ctrl+c event
process.on('SIGINT', exitHandler.bind(null, {
	exit: true
}));

//catches uncaught exceptions
process.on('uncaughtException', exitHandler.bind(null, {
	exit: true
}));

/*******************************************
 * Start rf_duino_node_test scenario
 *******************************************/

debug('starting rf_duino_node_test');

async.series([
function (callback) {
	RFDuino.discover(function (error, discoveredRFDuino) {
		debug('rf_duino_node with uuid ' + discoveredRFDuino._uuid + ' discovered');
		rfDuino = discoveredRFDuino;
		callback();
	});
},

function (callback) {
	debug('connect to rf_duino_node');
	rfDuino.connect(function () {
		debug('connected to rf_duino_node');
		callback();
	});
},

function (callback) {
	debug('discover rf_duino_node services');
	rfDuino.discoverServicesAndCharacteristics(function () {
		debug('rf_duino_node services discovered');
		callback();
	});
},

function (callback) {
	rfDuino.readDeviceName(function (deviceName) {
		debug('rf_duino_node name is ' + deviceName);
		callback();
	});
},

function (callback) {
	debug('notify for new data');

	/** PREREQUISITIES : Some data must written on discovered RFDuino using serial interface */
	rfDuino.on('dataReceived', function (data) {
		debug('data received : ');
		for (var index = 0; index < data.length; index++) {
			debug('0x' + data[index].toString(16) + ' ');
		}
	});
	rfDuino.notifyDataReceive(function () {
		debug('you will be notified on new data');
		callback();
	});
}],

function (error, results) {
	if (error) {
		debug('rf_duino_node test : FAILED - error : ' + error + ' - exiting test...');
		cleanRFDuino();
	} else {
		debug('rf_duino_node test - SUCCESS');
	}
});
