import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { IonicModule } from '@ionic/angular';

import { PinoutComponent } from './pinout.component';

describe('PinoutComponent', () => {
  let component: PinoutComponent;
  let fixture: ComponentFixture<PinoutComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PinoutComponent ],
      imports: [IonicModule.forRoot()]
    }).compileComponents();

    fixture = TestBed.createComponent(PinoutComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  }));

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
