/* Focused regression for category selection and bookmark restoration. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const source = fs.readFileSync(path.join(__dirname, '../site/script.js'), 'utf8');
const categories = ['equipment', 'maintenance', 'operations', 'safety', 'people', 'documents', 'control'];

function createPage(hash = '') {
  const location = {hash};
  const windowEvents = new Map();
  function element(id, dataset = {}) {
    const events = new Map();
    const attributes = new Map();
    return {
      id, dataset, events, attributes, hidden: false,
      setAttribute(name, value) { attributes.set(name, value); },
      addEventListener(name, handler) { events.set(name, handler); },
      focus() {},
      scrollIntoView() {}
    };
  }
  const tabs = categories.map(id => element(`tab-${id}`, {panel: id}));
  const panels = categories.map(id => element(`panel-${id}`));
  const tablist = element('tabs');
  const crosslink = element('crosslink', {showPanel: 'documents'});
  const document = {
    querySelectorAll(selector) {
      if (selector === '.platform-choice') return tabs;
      if (selector === '.platform-panel') return panels;
      if (selector === '[data-show-panel]') return [crosslink];
      return [];
    },
    querySelector(selector) { return selector === '.platform-tabs' ? tablist : null; },
    documentElement: {classList: {add() {}}}
  };
  const context = {
    document, location,
    history: {replaceState(state, title, url) { location.hash = url; }},
    window: {addEventListener(name, handler) { windowEvents.set(name, handler); }}
  };
  vm.runInNewContext(source, context);
  function activate(id, event = 'click', key) {
    const target = tabs.find(tab => tab.dataset.panel === id);
    target.events.get(event)({key, preventDefault() {}});
  }
  function selected(id) {
    assert.equal(tabs.find(tab => tab.dataset.panel === id).attributes.get('aria-selected'), 'true');
    assert.deepEqual(panels.filter(panel => !panel.hidden).map(panel => panel.id), [`panel-${id}`]);
  }
  return {location, windowEvents, crosslink, activate, selected};
}

const page = createPage('#panel-maintenance');
page.selected('maintenance');
page.activate('safety');
assert.equal(page.location.hash, '#panel-safety');
page.selected('safety');
createPage(page.location.hash).selected('safety');
page.activate('control', 'keydown', 'Enter');
assert.equal(page.location.hash, '#panel-control');
page.selected('control');
page.activate('equipment', 'keydown', ' ');
assert.equal(page.location.hash, '#panel-equipment');
page.selected('equipment');
page.crosslink.events.get('click')({preventDefault() {}});
assert.equal(page.location.hash, '#panel-documents');
page.selected('documents');
page.location.hash = '#panel-people';
page.windowEvents.get('hashchange')();
page.selected('people');
createPage('#contact').selected('equipment');
console.log('PASS: mouse, keyboard, crosslink, hash change and bookmark restoration');
