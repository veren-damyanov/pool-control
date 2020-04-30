import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, of } from "rxjs";
import { SettingsService } from './settings.service';

@Injectable({
	providedIn: 'root'
})
export class DeviceService {

	headers: HttpHeaders;

	constructor(private http: HttpClient, private settingsService: SettingsService) { }

	getHeaders() {
		return new HttpHeaders({
			'Accept': 'application/json',
			'Content-Type': 'application/json',
		});
	}

	getDevices(): Observable<Object> {
		var headers = this.getHeaders()
		return this.http.get<any>(this.settingsService.getUrl() + '/devices', { headers })
	}

	getAvailable(): Observable<Object> {
		var headers = this.getHeaders()
		return this.http.get<any>(this.settingsService.getUrl() + '/devices/available', { headers })
	}

	getInUse(): Observable<Object> {
		var headers = this.getHeaders()
		return this.http.get<any>(this.settingsService.getUrl() + '/devices/inuse', { headers })
	}

	createDevice(form): Observable<Object> {
		var headers = this.getHeaders()
		return this.http.post<any>(this.settingsService.getUrl() + '/devices', form.value, { headers })
	}

	editDevice(form): Observable<Object> {
		var headers = this.getHeaders()
		return this.http.put<any>(this.settingsService.getUrl() + '/devices/' + form.value.name, form.value, { headers })
	}

	deleteDevice(name): Observable<Object> {
		var headers = this.getHeaders()
		return this.http.delete<any>(this.settingsService.getUrl() + '/devices/' + name, { headers })
	}

}
