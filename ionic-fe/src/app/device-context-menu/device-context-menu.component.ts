import { Component, OnInit } from '@angular/core';
import { ModalController, PopoverController } from '@ionic/angular';

import { DeviceFormComponent } from '../device-form/device-form.component';
import { DeviceService } from '../device.service';
import { gnotify } from '../events';


@Component({
	selector: 'app-device-context-menu',
	templateUrl: './device-context-menu.component.html',
	styleUrls: ['./device-context-menu.component.scss'],
})
export class DeviceContextMenuComponent implements OnInit {

	private notify = gnotify;
	private device;
	private available;

	constructor(private deviceService: DeviceService, public popoverController: PopoverController, public modalController: ModalController) { }

	ngOnInit() { }

	deleteDevice() {
		console.debug("deleteDevice() called")
		this.deviceService.deleteDevice(this.device.name).subscribe(data => {
		}, err => {
			console.error('Delete record failed.', err)
		});
		this.notify.emit('reload-device');
		this.popoverController.dismiss()
	}

	async presentDeviceFormModal() {
		console.info("presentDeviceFormModal() creating device form modal from context menu")
		const modal = await this.modalController.create({
			component: DeviceFormComponent,
			componentProps: { 'device': this.device, 'operation': 'edit', 'available': this.available }
		});
		var result = await modal.present();
		this.popoverController.dismiss()
		return result
	}

}
