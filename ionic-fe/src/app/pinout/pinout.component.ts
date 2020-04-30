import { Component, OnInit } from '@angular/core';
import { SettingsService } from '../settings.service';

@Component({
	selector: 'app-pinout',
	templateUrl: './pinout.component.html',
	styleUrls: ['./pinout.component.scss'],
})
export class PinoutComponent implements OnInit {

	public ipAddr = this.settingsService.getIP()
	public port = this.settingsService.getPort()

	constructor(private settingsService: SettingsService) { }

	ngOnInit() { }

}
