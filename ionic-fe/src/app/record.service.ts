import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from "rxjs";
import { SettingsService } from './settings.service';


@Injectable({
	providedIn: 'root'
})
export class RecordService {

	headers: HttpHeaders;

	constructor(private http: HttpClient, private settingsService: SettingsService) { }

	getHeaders() {
		return new HttpHeaders({
			'Accept': 'application/json',
			'Content-Type': 'application/json',
		});
	}

	getRecords(): Observable<Object[]> {
		var headers = this.getHeaders()
		return this.http.get<any>(this.settingsService.getUrl() + '/records', { headers });
	}

	createRecord(form): Observable<Object[]> {
		var headers = this.getHeaders()
		return this.http.post<any>(this.settingsService.getUrl() + '/records', form.value, { headers })
	}

	editRecord(form): Observable<Object[]> {
		var headers = this.getHeaders()
		var pkey = form['controls']['pkey']['value']
		return this.http.put<any>(this.settingsService.getUrl() + '/records/' + pkey, form.value, { headers })
	}
	deleteRecord(pkey) {
		var headers = this.getHeaders()
		return this.http.delete<any>(this.settingsService.getUrl() + '/records/' + pkey, { headers })
	}
}
