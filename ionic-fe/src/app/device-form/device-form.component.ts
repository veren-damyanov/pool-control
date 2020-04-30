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
			device = { 'name': firstName, 'gpio': firstGpio };
		}
		if (this.operation == 'edit') {
			device = this.device;
			this.available['gpios'].unshift(device.gpio);
			this.available['gpios'].sort((x, y) => { return +x - +y });
		}
		this.populateForm(device);
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
