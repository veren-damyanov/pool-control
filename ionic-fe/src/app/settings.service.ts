import { Injectable } from '@angular/core';

@Injectable({
	providedIn: 'root'
})

export class SettingsService {

	constructor() { }

	getIP() {
		return localStorage.getItem("ip");
	}

	setIP(newIP) {
		localStorage.setItem("ip", newIP)
	}

	getPort() {
		return localStorage.getItem("port");
	}

	setPort(newPort) {
		localStorage.setItem("port", newPort)
	}

	setTimepickerInterval(newInterval) {
		localStorage.setItem("timepickerInterval", newInterval)
	}

	getTimepickerInterval() {
		return localStorage.getItem("timepickerInterval");
	}

	getUrl() {
		return 'http://' + this.getIP() + ':' + this.getPort() + '/api';
	}
}
