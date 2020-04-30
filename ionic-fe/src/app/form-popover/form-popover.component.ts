import { Component, OnInit } from '@angular/core';
import { RecordService } from '../record.service';
import { pickerController } from '@ionic/core';
import { Validators, FormBuilder, FormGroup } from '@angular/forms';
import { Output, EventEmitter } from '@angular/core';
import { ModalController } from '@ionic/angular';

import { gnotify } from '../events';
import { DeviceService } from '../device.service';
import { SettingsService } from '../settings.service';


@Component({
	selector: 'app-form-popover',
	templateUrl: './form-popover.component.html',
	styleUrls: ['./form-popover.component.scss'],
})
export class FormPopoverComponent implements OnInit {

	@Output() notify = gnotify;

	private record;
	private operation;

	private powerOptions = [[0, 25, 50, 75, 100]];
	private tempOptions = [[70, 72, 74, 76, 78, 80, 82, 84, 86, 88, 90]];
	private relayOptions = [['OFF', 'ON']];
	public form;
	public inUse;
	public valueButtonName;
	public valueOptions;
	public timepickerList;


	constructor(private recordService: RecordService, private settingsService: SettingsService, private formBuilder: FormBuilder, public modalController: ModalController) { }

	ngOnInit() { 
		var record;
		if (this.operation == 'create') {
			var firstTarget = this.inUse[0];
			var targetValue = this.getDefaultForTarget(firstTarget)
			record = {'pkey': '', 'target': firstTarget, 'value': targetValue,
					'start_at': '1990-02-19T08:00+02:00', 'end_at': '1990-02-19T20:00+02:00',
					'dow': ['MO','TU','WE','TH','FR']}
		}
		if (this.operation == 'edit') {
			record = this.record
		}
		this.configureTimepicker();
		this.populateForm(record);
		this.onTargetChange(record.target);
	}

	populateForm(record) {
		console.debug("pupulateForm() called")
		this.form = this.formBuilder.group({
			pkey: [record.pkey, Validators.required],
			target: [record.target, Validators.required],
			value: [record.value, Validators.required],
			start_at: [record.start_at, Validators.required],
			end_at: [record.end_at, Validators.required],
			dow: [record.dow, Validators.required],
		});
	}
	
	configureTimepicker() {
		console.debug("configureTimepicker() called")
		var pickerInterval = this.settingsService.getTimepickerInterval();
		if (!pickerInterval || pickerInterval == "1") {
			this.timepickerList = "";
		} else if (pickerInterval == "5") {
			this.timepickerList = "0,5,10,15,20,25,30,35,40,45,50,55";
		} else if (pickerInterval == "10") {
			this.timepickerList = "0,10,20,30,40,50";
		} else if (pickerInterval == "15") {
			this.timepickerList = "0,15,30,45";
		}
	}

	padTime(time) {
		console.debug("padTime() called")
		return ("00" + time).slice(-2)
	}

	submitForm() {
		console.info("submitForm() called for schedule form")
		if (this.operation == 'create') {
			this.recordService.createRecord(this.form).subscribe(data => {
			}, err => {
				console.error('Creating record failed.', err)
			});
		} else if (this.operation == 'edit') {
			this.recordService.editRecord(this.form).subscribe(data => {
			}, err => {
				console.error('Editing record failed.', err)
			});
		} else {
			throw Error('UNREACHABLE')
		}

		this.notify.emit('reload')
		this.cancelModal()
	}

	cancelModal() {
		console.debug("cancelModal() called")
		this.modalController.dismiss();
	}

	async openPicker(numColumns = 1, numOptions = 5, columnOptions) {
		console.debug("openPicker() called")
		const picker = await pickerController.create({
			columns: this.getColumns(numColumns, numOptions, columnOptions),
			buttons: [
				{
					text: 'Cancel',
					role: 'cancel'
				},
				{
					text: 'Confirm',
					handler: (value) => {
						(document.getElementById('valueInput') as HTMLInputElement).value = value['col-0']['text']
					}
				}
			]
		});
		await picker.present();
	}

	getColumns(numColumns, numOptions, columnOptions) {
		console.debug("getColumns() called")
		let columns = [];
		for (let i = 0; i < numColumns; i++) {
			columns.push({
				name: `col-${i}`,
				options: this.getColumnOptions(i, numOptions, columnOptions)
			});
		}
		return columns;
	}

	getColumnOptions(columnIndex, numOptions, columnOptions) {
		console.debug("getColumnOptions() called")
		let options = [];
		for (let i = 0; i < numOptions; i++) {
			options.push({
				text: columnOptions[columnIndex][i % numOptions],
				value: i
			})
		}
		return options;
	}

	getDefaultForTarget(target) {
		console.debug("getDefaultForTarget() called")
		target = target.slice(0, 1);
		if (target == "P" || target == "L") {
			return "50";
		} else if (target == "T") {
			return "80";
		} else if (target == "D") {
			return "ON";
		}
	}

	onTargetChange(target) {
		console.debug("onTargetChange() called")
		var targetType = target.slice(0, 1);
		var defaultValue = this.getDefaultForTarget(targetType);
		if (targetType == 'P' || targetType == 'L') {
			this.valueOptions = this.powerOptions;
			this.valueButtonName = 'Power';
			(document.getElementById('valueInput') as HTMLInputElement).value = defaultValue;
		}
		if (targetType == 'T') {
			this.valueOptions = this.tempOptions;
			this.valueButtonName = 'Temperature';
			(document.getElementById('valueInput') as HTMLInputElement).value = defaultValue;
		}
		if (targetType == 'D') {
			this.valueOptions = this.relayOptions;
			this.valueButtonName = 'Toggle';
			(document.getElementById('valueInput') as HTMLInputElement).value = defaultValue;
		} else {
		}
	}

}
