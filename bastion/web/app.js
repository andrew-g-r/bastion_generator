'use strict';
const form = document.querySelector('#generator');
const status = document.querySelector('#status');
const results = document.querySelector('#results');
let characters = [];
function element(tag, text, className) {
  const item = document.createElement(tag);
  if (text !== undefined) item.textContent = text;
  if (className) item.className = className;
  return item;
}
function display() {
  results.replaceChildren();
  document.querySelector('#download').disabled = !characters.length;
  document.querySelector('#print').disabled = !characters.length;
  for (const c of characters) {
    const card = element('article');
    card.append(element('h2', c.name), element('h3', c.career));
    const abilities = element('div', undefined, 'abilities');
    ['STR', 'DEX', 'CHA'].forEach((name, i) => abilities.append(element('span', `${name} ${c.abilities[i]}`)));
    abilities.append(element('span', `HP ${c.hp}`), element('span', `£${c.money}`));
    card.append(abilities, element('p', c.description), element('p', c.equipment));
    c.prompts.forEach((prompt, i) => card.append(element('h3', prompt), element('p', c.answers[i])));
    card.append(element('h3', 'Group debt · if youngest'), element('p', c.debt));
    results.append(card);
  }
}
form.addEventListener('submit', async event => {
  event.preventDefault();
  const button = form.querySelector('button');
  button.disabled = true;
  status.textContent = 'Rolling…';
  try {
    const values = new URLSearchParams();
    for (const [key, value] of new FormData(form)) if (value !== '') values.set(key, value);
    values.set('random_name', String(form.elements.random_name.checked));
    const response = await fetch(`/api/generate?${values}`);
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'Generation failed');
    characters = data;
    display();
    status.textContent = `${characters.length} character${characters.length === 1 ? '' : 's'} ready.`;
  } catch (error) { status.textContent = error.message; }
  finally { button.disabled = false; }
});
fetch('/api/careers').then(response => response.json()).then(careers => {
  for (const career of careers) {
    const option = element('option', career.title);
    option.value = career.id;
    document.querySelector('#career').append(option);
  }
}).catch(() => { status.textContent = 'Could not load careers. Refresh to try again.'; });

document.querySelector('#download').addEventListener('click', () => {
  const url = URL.createObjectURL(new Blob([JSON.stringify(characters, null, 2)], {type:'application/json'}));
  const link = element('a');
  link.href = url; link.download = 'bastion-party.json'; link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
});
document.querySelector('#print').addEventListener('click', () => window.print());

document.querySelector('#save-roster').addEventListener('click', () => {
  try {
    if (!characters.length) throw new Error('Roll a party first.');
    localStorage.setItem('bastion-party-v1', JSON.stringify(characters));
    status.textContent = 'Party saved in this browser.';
  } catch (error) { status.textContent = error.message; }
});
document.querySelector('#load-roster').addEventListener('click', () => {
  try {
    const saved = localStorage.getItem('bastion-party-v1');
    if (!saved) throw new Error('No party has been saved in this browser.');
    characters = validateCharacters(JSON.parse(saved)); display();
    status.textContent = 'Saved party restored.';
  } catch (error) { status.textContent = error.message; }
});
document.querySelector('#clear-roster').addEventListener('click', () => {
  try { localStorage.removeItem('bastion-party-v1'); status.textContent = 'Saved party removed from this browser.'; }
  catch (error) { status.textContent = error.message; }
});
function validateCharacters(data) {
  const items = Array.isArray(data) ? data : [data];
  if (!items.length || items.length > 20) throw new Error('Load between 1 and 20 characters.');
  for (const c of items) {
    if (!c || c.schema_version !== 1 || !Array.isArray(c.abilities) || c.abilities.length !== 3 ||
        !c.abilities.every(a => Number.isInteger(a) && a >= 3 && a <= 18) ||
        !Number.isInteger(c.hp) || c.hp < 1 || c.hp > 6 || !Number.isInteger(c.money) || c.money < 1 || c.money > 6 ||
        !Array.isArray(c.prompts) || c.prompts.length !== 2 || !Array.isArray(c.answers) || c.answers.length !== 2 ||
        ![c.name,c.career,c.description,c.equipment,c.debt,...c.prompts,...c.answers].every(v => typeof v === 'string')) {
      throw new Error('Invalid character file. Use a version 1 Bastion JSON export.');
    }
  }
  return items;
}
