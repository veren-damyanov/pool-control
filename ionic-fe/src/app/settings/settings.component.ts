import { Component, OnInit } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { SettingsService } from '../settings.service';

@Component({
	selector: 'app-settings',
	templateUrl: './settings.component.html',
	styleUrls: ['./settings.component.scss'],
})
export class SettingsComponent implements OnInit {

	public form;

	constructor(private formBuilder: FormBuilder, private settingsService: SettingsService) { }

	ngOnInit() {
		var timepickerInterval = this.settingsService.getTimepickerInterval()
		if (!timepickerInterval) {
			timepickerInterval = "1";
		}
		this.form = this.formBuilder.group({
			ip: this.settingsService.getIP(),
			port: this.settingsService.getPort(),
			timepicker: timepickerInterval,
		});
	}

	submitForm() {
		console.info("submitForm() called for settings form")
		this.settingsService.setIP(this.form.value.ip);
		this.settingsService.setPort(this.form.value.port);
		this.settingsService.setTimepickerInterval(this.form.value.timepicker);
	}
}
