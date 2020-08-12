import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ShowAlignmentComponent } from './show-alignment.component';

describe('ShowAlignmentComponent', () => {
    let component: ShowAlignmentComponent;
    let fixture: ComponentFixture<ShowAlignmentComponent>;

    beforeEach(
        async(() => {
            TestBed.configureTestingModule({
                declarations: [ShowAlignmentComponent]
            }).compileComponents();
        })
    );

    beforeEach(() => {
        fixture = TestBed.createComponent(ShowAlignmentComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });
});
