import { PopupModalModule } from './popup-modal.module';

describe('PopupModalModule', () => {
  let popup-modalModule: PopupModalModule;

  beforeEach(() => {
    popup-modalModule = new PopupModalModule();
  });

  it('should create an instance', () => {
    expect(popup-modalModule).toBeTruthy();
  });
});
