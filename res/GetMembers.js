var xpath = (p, c) => {
	return document.evaluate(p, c??document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
};

var adduser = (e) => {
	e = e.target ?? e;
	if(e.classList.toString().includes('member-')){
		let id = xpath('.//img', e);
		if(id == null) return;
		id = id.src.split('/');
		id = id[id.length - 2];
		if(isNaN(id)) return;
		users.add(id);
		canscroll = true;
	}
};

window.users = new Set();
var canscroll;
var scroller;
window.done = false;

var sc = xpath('//div[@aria-label="Members"]/..');
sc.addEventListener('DOMNodeInserted', adduser);

var m = document.evaluate('.//div[@aria-expanded="false"]', sc, null, XPathResult.UNORDERED_NODE_SNAPSHOT_TYPE, null);
for(var i = 0; i<m.snapshotLength; i++){
	adduser(m.snapshotItem(i));
}

canscroll = true;
scroller = setInterval(() => {
	if(!canscroll) return;
	canscroll = false;
	sc.scrollBy(0, sc.offsetHeight);
	if(sc.scrollHeight - sc.scrollTop == sc.offsetHeight){
		clearInterval(scroller);
		window.done = true;
	}
}, 300);