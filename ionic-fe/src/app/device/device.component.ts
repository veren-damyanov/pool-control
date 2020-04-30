import { Component, OnInit } from '@angular/core';
import { ModalController } from '@ionic/angular';

import { gnotify } from '../events';
import { DeviceService } from '../device.service';
import { DeviceFormComponent } from '../device-form/device-form.component';

@Component({
	selector: 'app-device',
	templateUrl: './device.component.html',
	styleUrls: ['./device.component.scss'],
})
export class DeviceComponent implements OnInit {

	private notify = gnotify
	public devices = null;
	public available: any = { "names": [], "gpios": [] };

	constructor(private deviceService: DeviceService, public modalController: ModalController) { }

	ngOnInit() {
		this.getDevices();
		this.getAvailable();
		this.notify.addListener('reload-device', () => {
			this.deviceService.getDevices().subscribe(data => {
				this.devices = data['devices'];
			}, err => {
				console.error('Fetching devices failed.', err);
			});
		});
		this.notify.addListener('reload-available', () => {
			this.deviceService.getAvailable().subscribe(data => {
				this.available = data;
			}, err => {
				console.error('Getting available devices failed.', err)
			});
		});
		document.querySelector('ion-content').scrollToBottom(300);

	}

	getDevices() {
		console.debug("getDevices() called")
		this.deviceService.getDevices().subscribe(data => {
			this.devices = data['devices'];
		}, err => {
			console.error('Fetching devices failed.', err)
		});
	}

	getAvailable() {
		console.debug("getAvailable() called")
		this.deviceService.getAvailable().subscribe(data => {
			this.available = data;
		}, err => {
			console.error('Getting available devices failed.', err)
		});
	}

	async presentDeviceFormModal() {
		console.info("presentDeviceFormModal() creating device form modal")
		const modal = await this.modalController.create({
			component: DeviceFormComponent,
			componentProps: { 'device': null, 'operation': 'create', 'available': this.available }
		});
		return await modal.present();
	}

}
