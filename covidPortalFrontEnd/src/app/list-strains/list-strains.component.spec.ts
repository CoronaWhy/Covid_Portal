import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ListStrainsComponent } from './list-strains.component';

describe('ListStrainsComponent', () => {
    let component: ListStrainsComponent;
    let fixture: ComponentFixture<ListStrainsComponent>;

    beforeEach(
        async(() => {
            TestBed.configureTestingModule({
                declarations: [ListStrainsComponent]
            }).compileComponents();
        })
    );

    beforeEach(() => {
        fixture = TestBed.createComponent(ListStrainsComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });
});
