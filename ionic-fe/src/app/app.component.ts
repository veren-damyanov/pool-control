import { Component, OnInit } from '@angular/core';

import { Platform } from '@ionic/angular';
import { SplashScreen } from '@ionic-native/splash-screen/ngx';
import { StatusBar } from '@ionic-native/status-bar/ngx';
import { ConsoleService } from './console.service';

@Component({
	selector: 'app-root',
	templateUrl: 'app.component.html',
	styleUrls: ['app.component.scss']
})
export class AppComponent implements OnInit {
	public selectedIndex = 0;
	public appPages = [
		{
			title: 'Schedule',
			url: '/schedule',
			icon: 'list'
		},
		{
			title: 'Devices',
			url: '/devices',
			icon: 'bulb'
		},
		{
			title: 'Pinout',
			url: '/pinout',
			icon: 'hardware-chip'
		},
		{
			title: 'Settings',
			url: '/settings',
			icon: 'settings'
		},
		{
			title: 'About',
			url: '/about',
			icon: 'information-circle'
		},

	];
	public labels = ['Family', 'Friends', 'Notes', 'Work', 'Travel', 'Reminders'];

	constructor(
		// private customConsole: ConsoleService,
		private platform: Platform,
		private splashScreen: SplashScreen,
		private statusBar: StatusBar
	) {
		this.initializeApp();
	}

	initializeApp() {
		this.platform.ready().then(() => {
			this.statusBar.styleDefault();
			this.splashScreen.hide();
		});
	}

	ngOnInit() {
		const path = window.location.pathname.split('folder/')[1];
		if (path !== undefined) {
			this.selectedIndex = this.appPages.findIndex(page => page.title.toLowerCase() === path.toLowerCase());
		}
	}
}
