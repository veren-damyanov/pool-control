import { Component, OnInit } from '@angular/core';
import { Validators, FormBuilder, FormGroup } from '@angular/forms';

import { gnotify } from '../events';
import { ModalController } from '@ionic/angular';
import { DeviceService } from '../device.service';


@Component({
	selector: 'app-device-form',
	templateUrl: './device-form.component.html',
	styleUrls: ['./device-form.component.scss'],
})
export class DeviceFormComponent implements OnInit {

	private notify = gnotify
	private device;
	public operation;
	public available;
	public form;

	constructor(private deviceService: DeviceService, private formBuilder: FormBuilder, public modalController: ModalController) { }

	ngOnInit() {
		var device
		if (this.operation == 'create') {
			var firstName = this.available.names[0];
			var firstGpio = this.available.gpios[0];
			device = { 'name': firstName, 'gpio': firstGpio, 'kind': this.getKind(firstName) };
		}
		if (this.operation == 'edit') {
			device = this.device;
			this.available['gpios'].unshift(device.gpio);
			this.available['gpios'].sort((x, y) => { return +x - +y });
		}
		this.populateForm(device);
	}

	getKind(deviceName) {
		console.debug('getKind() called')
		var deviceKind = deviceName.slice(0, 1);
		if (deviceKind == 'P') {
			return 'pump'
		} else if (deviceKind == 'L') {
			return 'light'
		} else if (deviceKind == 'D') {
			return 'relay'
		} else if (deviceKind == 'T') {
			return 'heat' // FIXME: Not supported by backend yet!
		}
	}
	onDeviceChange(deviceName) {
		console.debug('onDeviceChange() called')
		var kind = this.getKind(deviceName)
		this.form.controls.kind.value = kind
	}

	cancelModal() {
		console.debug("cancelModal() called")
		this.modalController.dismiss();
		this.notify.emit('reload-available');
	}

	populateForm(device) {
		console.debug("populateForm() called")
		this.form = this.formBuilder.group({
			name: [device.name, Validators.required],
			gpio: [device.gpio.toString(), Validators.required],
			kind: [device.kind, Validators.required]
		});
	}

	submitForm() {
		console.info("submitForm() called for device form")
		if (this.operation == 'create') {
			this.deviceService.createDevice(this.form).subscribe(data => {
			}, err => {
				console.error('Creating device failed.', err)
			});

		} else if (this.operation == 'edit') {
			this.deviceService.editDevice(this.form).subscribe(data => {
			}, err => {
				console.error('Editing device failed.', err)
			});

		} else {
			throw Error('UNREACHABLE')
		}

		this.notify.emit('reload-device')
		this.notify.emit('reload-available');
		this.cancelModal()
	}

}
