import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TestDatatableComponent } from './test-datatable.component';

describe('TestDatatableComponent', () => {
    let component: TestDatatableComponent;
    let fixture: ComponentFixture<TestDatatableComponent>;

    beforeEach(
        async(() => {
            TestBed.configureTestingModule({
                declarations: [TestDatatableComponent]
            }).compileComponents();
        })
    );

    beforeEach(() => {
        fixture = TestBed.createComponent(TestDatatableComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });
});
