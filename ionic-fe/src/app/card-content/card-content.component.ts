import { Component, OnInit, Input } from '@angular/core';
import { RecordService } from '../record.service';
import { ModalController } from '@ionic/angular';
import { gnotify } from '../events';
import { FormPopoverComponent } from '../form-popover/form-popover.component';
import { DeviceService } from '../device.service';
import { SettingsService } from '../settings.service';


@Component({
	selector: 'app-card-content',
	templateUrl: './card-content.component.html',
	styleUrls: ['./card-content.component.scss'],
})
export class CardContentComponent implements OnInit {

	private notify = gnotify;
	public inUse = null;
	public records = null;
	private popover = null;

	constructor(private recordService: RecordService, private deviceService: DeviceService, public modalController: ModalController) { }

	ngOnInit() {
		this.getRecords()
		this.deviceService.getInUse().subscribe(data => {
			this.inUse = data['names'];
		}, err => {
			console.error("Fetching devices in use failed: ", err)
		});
		this.notify.addListener('reload', () => {
			this.recordService.getRecords().subscribe(data => {
				this.records = data['records'];
			}, err => {
				console.error('Fetching records failed.', err)
			});
			this.deviceService.getInUse().subscribe(data => {
				this.inUse = data['names'];
			}, err => {
				console.error("Fetching devices in use failed: ", err)
			});
			document.querySelector('ion-content').scrollToBottom(300)
		})
	}

	getRecords(): void {
		console.debug("getRecords() called")
		this.recordService.getRecords().subscribe(data => {
			this.records = data['records'];
		}, err => {
			console.error('Fetching records failed.', err)
		});
	}

	async presentFormModal() {
		console.info("presentFormModal() creating form modal")
		const modal = await this.modalController.create({
			component: FormPopoverComponent,
			componentProps: { 'record': null, 'operation': 'create', 'inUse': this.inUse }
		});
		return await modal.present();
	}
}
