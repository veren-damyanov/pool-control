import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { SettingsService } from './settings.service';
import { Observable, of } from "rxjs";
import { ToastController } from '@ionic/angular';

import * as moment from 'moment';

const DATE_FMT_4LOG = 'YYYY-MM-DD HH:mm:ss,SSS Z';


/**
 * Replacement for the standnard console which sends log info
 * to the server via API calls.
 */
@Injectable({
	providedIn: 'root'
})
export class ConsoleService implements Console {
	memory: any;
	Console: NodeJS.ConsoleConstructor;

	private orig: Console;
	private user: object;

	constructor(private http: HttpClient, private settingsService: SettingsService, public toastController: ToastController) {
		if (!this.orig) {
			console.warn("REPLACING console object...")
			this.orig = console
			console = this
			this.orig.warn("REPLACED.")

		} else {
			console.error("Could NOT replace console - this.orig:", this.orig)
		}
	}

	markTimeline(label?: string): void {
		throw new Error("Method not implemented.");
	}
	timeStamp(label?: string): void {
		throw new Error("Method not implemented.");
	}
	timeline(label?: string): void {
		throw new Error("Method not implemented.");
	}
	timelineEnd(label?: string): void {
		throw new Error("Method not implemented.");
	}

	getHeaders() {
		return new HttpHeaders({
			'Accept': 'application/json',
			'Content-Type': 'application/json',
		});
	}

	postLogs(payload): Observable<Object> {
		var headers = this.getHeaders()
		return this.http.post<any>(this.settingsService.getUrl() + '/client-logs', payload, { headers })
	}

	async presentToast(args) {
		if (args[1].hasOwnProperty('statusText')) {
			args[1] = args[1].statusText
		}
		if (args[1].message && args[1].message.includes('URI is malformed')) {
			args = ['Could not connect to server']
		}
		const toast = await this.toastController.create({
			message: args.join(' '),
			duration: 5000
		});
		toast.present();
	}

	private _sendMessage(loglevel, args): void {
		console = this.orig  // switch to original console to avoid recursion
		const reqPayload = {
			'timestamp': moment().format(DATE_FMT_4LOG),
			'loglevel': loglevel,
			'args': args,
		}

		this.postLogs(reqPayload).subscribe(result => {
		}, err => {
			if (err.status !== 0) {  // if err.url is null, then the server is down
				console.error("Failed to send log message", err)
			}
		})
		if (loglevel == 'error') {
			this.presentToast(args)
		}
		console = this  // switch back to self as default console
	}

	getDevices(): Observable<Object> {
		var headers = this.getHeaders()
		return this.http.get<any>(this.settingsService.getUrl() + '/devices', { headers })
	}


	debug(...args: any[]) {
		this.orig.debug(...args)
		this._sendMessage('debug', args)
	}

	error(...args: any[]) {
		this.orig.error(...args)
		this._sendMessage('error', args)
	}

	exception(...args: any[]) {
		this.orig.exception(...args)
		this._sendMessage('exception', args)
	}

	info(...args: any[]) {
		this.orig.info(...args)
		this._sendMessage('info', args)
	}

	log(...args: any[]): void {
		this.orig.log(...args)
		this._sendMessage('log', args)
	}

	trace(...args: any[]) {
		this.orig.trace(...args)
		this._sendMessage('trace', args)
	}

	warn(...args: any[]) {
		this.orig.warn(...args)
		this._sendMessage('warn', args)
	}

	// ______________________________________________________________________
	// Non-overriden methods below

	assert(...args: any[]) {
		this.orig.assert(...args)
	}

	clear() {
		this.orig.clear()
	}

	count(countTitle?: string) {
		this.orig.count(countTitle)
	}

	dir(...args: any[]) {
		this.orig.dir(...args)
	}

	dirxml(value: any) {
		this.orig.dirxml(value)
	}

	group(...args: any[]) {
		this.orig.group(...args)
	}

	groupCollapsed(...args: any[]) {
		this.orig.groupCollapsed(...args)
	}

	groupEnd() {
		this.orig.groupEnd()
	}

	msIsIndependentlyComposed(element: Element): boolean {
		return false
	}

	profile(...args: any[]) {
		this.orig.profile(...args)
	}

	profileEnd(...args: any[]) {
		this.orig.profileEnd(...args)
	}

	// select(element: Element): void {
	// 	this.orig.select(element)
	// }

	table(...args: any[]) {
		this.orig.table(...args)
	}

	time(...args: any[]) {
		this.orig.time(...args)
	}

	timeEnd(...args: any[]) {
		this.orig.timeEnd(...args)
	}

}
