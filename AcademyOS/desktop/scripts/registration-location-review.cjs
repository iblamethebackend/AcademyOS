const assert = require('node:assert/strict');
const fs = require('node:fs');
const ts = require('typescript');

// Load the small, framework-independent registration modules with local TypeScript.
require.extensions['.ts'] = (module, filename) => {
  const source = fs.readFileSync(filename, 'utf8');
  module._compile(ts.transpileModule(source, {
    compilerOptions: {module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2020},
  }).outputText, filename);
};

const {validSchoolTimezone, validSchoolAddress, schoolTimezones} = require('../src/lib/school-timezones.ts');
const {makeRegisteredState, createSchoolPreview, registeredSetupKey} = require('../src/lib/school-registration.ts');
const {initialState} = require('../src/lib/model.ts');
const storage = new Map();
global.localStorage = {
  getItem: key => storage.get(key) ?? null,
  setItem: (key, value) => storage.set(key, value),
  removeItem: key => storage.delete(key),
};

const school = {
  ownerName: 'Test Owner', email: 'owner@example.com', name: 'Example School',
  slug: 'location-test', board: 'Other', city: 'London', phone: '+44 20 7946 0958',
  timezone: 'Europe/London', address: '  10 Example Road, London, UK  ',
};

assert.equal(validSchoolTimezone(''), false);
assert.equal(validSchoolTimezone('Asia/Unknown'), false);
assert.equal(validSchoolTimezone(undefined), false);
for (const timezone of ['Asia/Kolkata', 'Europe/London', 'America/New_York', 'UTC']) {
  assert.equal(validSchoolTimezone(timezone), true);
  assert.ok(schoolTimezones.includes(timezone));
}
assert.equal(validSchoolAddress('   '), false);
assert.equal(validSchoolAddress('a'.repeat(501)), false);
assert.equal(validSchoolAddress(school.address), true);
assert.throws(() => createSchoolPreview({...school, timezone: 'Invalid/Zone'}), /address/);
assert.throws(() => createSchoolPreview({...school, address: ''}), /address/);
assert.equal(storage.size, 0, 'Invalid registration must not be stored');

createSchoolPreview(school);
const saved = JSON.parse(localStorage.getItem(registeredSetupKey(school.slug)));
assert.equal(saved.school.timezone, 'Europe/London');
assert.equal(saved.school.address, '10 Example Road, London, UK');
assert.equal(makeRegisteredState({...school, timezone: 'America/New_York'}).school.timezone, 'America/New_York');
createSchoolPreview({...school,slug:'address-only',timezone:undefined});
const addressOnly=JSON.parse(localStorage.getItem(registeredSetupKey('address-only')));
assert.equal(addressOnly.school.address,'10 Example Road, London, UK');
assert.equal(addressOnly.school.timezone,'','Do not infer a school timezone');
assert.equal(initialState.school.timezone, 'Asia/Kolkata', 'Registration must not mutate fixtures');
console.log('PASS: required address, address-only registration, legacy timezone compatibility, persistence and fixture isolation.');
