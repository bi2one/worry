/**
 * @fileoverview 
 *  Tool '특수문자' Source,
 * Class Trex.Tool.SpecialChar 와 configuration을 포함    
 *     
 */

TrexMessage.addMsg({
	'@specialchar.subtitle1': '일반기호',
	'@specialchar.subtitle2': '수학부호, 통화단위',
	'@specialchar.subtitle3': '원 기호, 괄호',
	'@specialchar.subtitle4': '일본어',
	'@specialchar.subtitle5': '로마자, 그리스'
});

TrexConfig.addTool(
	"specialchar", 
	{
		sync: false,
		status: true,
		rows: 9,
		cols: 20,
		top: null,
		left: null,
		matrices: [{
			title: TXMSG('@specialchar.subtitle1'),
			options: ['\uff03', '\uff06', '\uff0a', '\uff20', '\xa7', '\u203b', '\u2606', '\u2605', '\u25cb', '\u25cf', '\u25ce', '\u25c7', '\u25c6', '\u25a1', '\u25a0', '\u25b3', '\u25b2', '\u25bd', '\u25bc', '\u2192', '\u2190', '\u2191', '\u2193', '\u2194', '\u3013', '\u25c1', '\u25c0', '\u25b7', '\u25b6', '\u2664', '\u2660', '\u2661', '\u2665', '\u2667', '\u2663', '\u2299', '\u25c8', '\u25a3', '\u25d0', '\u25d1', '\u2592', '\u25a4', '\u25a5', '\u25a8', '\u25a7', '\u25a6', '\u25a9', '\u2668', '\u260f', '\u260e', '\u261c', '\u261e', '\xb6', '\u2020', '\u2021', '\u2195', '\u2197', '\u2199', '\u2196', '\u2198', '\u266d', '\u2669', '\u266a', '\u266c', '\u327f', '\u321c', '\u2116', '\u33c7', '\u2122', '\u33c2', '\u33d8', '\u2121', '\xae', '\xaa', '\xba', '\uff02', '\uff08', '\uff09', '\uff3b', '\uff3d', '\uff5b', '\uff5d', '\u2018', '\u2019', '\u201c', '\u201d', '\u3014', '\u3015', '\u3008', '\u3009', '\u300a', '\u300b', '\u300c', '\u300d', '\u300e', '\u300f', '\u3010', '\u3011', '\uff01', '\uff07', '\uff0c', '\uff0e', '\uff0f', '\uff1a', '\uff1b', '\uff1f', '\uff3e', '\uff3f', '\uff40', '\uff5c', '\uffe3', '\u3001', '\u3002', '\xb7', '\u2025', '\u2026', '\xa8', '\u3003', '\u2015', '\u2225', '\uff3c', '\u223c', '\xb4', '\uff5e', '\u02c7', '\u02d8', '\u02dd', '\u02da', '\u02d9', '\xb8', '\u02db', '\xa1', '\xbf', '\u02d0']
		},{
			title: TXMSG('@specialchar.subtitle2'),
			options: ['\uff0b', '\uff0d', '\uff1c', '\uff1d', '\uff1e', '\xb1', '\xd7', '\xf7', '\u2260', '\u2264', '\u2265', '\u221e', '\u2234', '\u2642', '\u2640', '\u2220', '\u22a5', '\u2312', '\u2202', '\u2207', '\u2261', '\u2252', '\u226a', '\u226b', '\u221a', '\u223d', '\u221d', '\u2235', '\u222b', '\u222c', '\u2208', '\u220b', '\u2286', '\u2287', '\u2282', '\u2283', '\u222a', '\u2229', '\u2227', '\u2228', '\uffe2', '\u21d2', '\u21d4', '\u2200', '\u2203', '\u222e', '\u2211', '\u220f\uff04', '\uff05', '\uffe6', '\uff26', '\u2032', '\u2033', '\u2103', '\u212b', '\uffe0', '\uffe1', '\uffe5', '\xa4', '\u2109', '\u2030', '?', '\u3395', '\u3396', '\u3397', '\u2113', '\u3398', '\u33c4', '\u33a3', '\u33a4', '\u33a5', '\u33a5', '\u33a6', '\u3399', '\u339a', '\u339b', '\u339c', '\u339d', '\u339e', '\u339f', '\u33a0', '\u33a1', '\u33a2', '\u33ca', '\u338d', '\u338e', '\u338f', '\u33cf', '\u3388', '\u3389', '\u33c8', '\u33a7', '\u33a8', '\u33b0', '\u33b1', '\u33b2', '\u33b3', '\u33b4', '\u33b5', '\u33b6', '\u33b7', '\u33b8', '\u33b9', '\u3380', '\u3381', '\u3382', '\u3383', '\u3384', '\u33ba', '\u33bb', '\u33bc', '\u33bd', '\u33be', '\u33bf', '\u3390', '\u3391', '\u3392', '\u3393', '\u3394', '\u2126', '\u33c0', '\u33c1', '\u338a', '\u338b', '\u338c', '\u33d6', '\u33c5', '\u33ad', '\u33ae', '\u33af', '\u33db', '\u33a9', '\u33aa', '\u33ab', '\u33ac', '\u33dd', '\u33d0', '\u33d3', '\u33c3', '\u33c9', '\u33dc', '\u33c6']
		},{
			title: TXMSG('@specialchar.subtitle3'),
			options: [
				'\u3260', '\u3261', '\u3262', '\u3263', '\u3264', '\u3265', '\u3266', '\u3267', '\u3268', '\u3269',
				'\u326a', '\u326b', '\u326c', '\u326d', '\u326e', '\u326f', '\u3270', '\u3271', '\u3272', '\u3273',
				'\u3274', '\u3275', '\u3276', '\u3277', '\u3278', '\u3279', '\u327a', '\u327b', '\u3200', '\u3201',
				'\u3202', '\u3203', '\u3204', '\u3205', '\u3206', '\u3207', '\u3208', '\u3209', '\u320a', '\u320b', 
				'\u320c', '\u320d', '\u320e', '\u320f', '\u3210', '\u3211', '\u3212', '\u3213', '\u3214', '\u3215', 
				'\u3216', '\u3217', '\u3218', '\u3219', '\u321a', '\u321b', '\u24d0', '\u24d1', '\u24d2', '\u24d3', 
				'\u24d4', '\u24d5', '\u24d6', '\u24d7', '\u24d8', '\u24d9', '\u24da', '\u24db', '\u24dc', '\u24dd', 
				'\u24de', '\u24df', '\u24e0', '\u24e1', '\u24e2', '\u24e3', '\u24e4', '\u24e5', '\u24e6', '\u24e7', '\u24e8', '\u24e9', '\u2460', '\u2461', '\u2462', '\u2463', '\u2464', '\u2465', '\u2466', '\u2467', '\u2468', '\u2469', '\u246a', '\u246b', '\u246c', '\u246d', '\u246e', '\u249c', '\u249d', '\u249e', '\u249f', '\u24a0', '\u24a1', '\u24a2', '\u24a3', '\u24a4', '\u24a5', '\u24a6', '\u24a7', '\u24a8', '\u24a9', '\u24aa', '\u24ab', '\u24ac', '\u24ad', '\u24ae', '\u24af', '\u24b0', '\u24b1', '\u24b2', '\u24b3', '\u24b4', '\u24b5', '\u2474', '\u2475', '\u2476', '\u2477', '\u2478', '\u2479', '\u247a', '\u247b', '\u247c', '\u247d', '\u247e', '\u247f', '\u2480', '\u2481', '\u2482']
		},{
			title: TXMSG('@specialchar.subtitle4'),
			options: ['\u3041', '\u3042', '\u3043', '\u3044', '\u3045', '\u3046', '\u3047', '\u3048', '\u3049', '\u304a', '\u304b', '\u304c', '\u304d', '\u304e', '\u304f', '\u3050', '\u3051', '\u3049', '\u3053', '\u3054', '\u3055', '\u3056', '\u3057', '\u3058', '\u3059', '\u305a', '\u305b', '\u305c', '\u305d', '\u305e', '\u305f', '\u3060', '\u3061', '\u3062', '\u3063', '\u3064', '\u3065', '\u3066', '\u3067', '\u3068', '\u3069', '\u306a', '\u306b', '\u306c', '\u306d', '\u306e', '\u306f', '\u3070', '\u3071', '\u3072', '\u3073', '\u3074', '\u3075', '\u3076', '\u3077', '\u3078', '\u3079', '\u307a', '\u307b', '\u307c', '\u307d', '\u307e', '\u307f', '\u3080', '\u3081', '\u3082', '\u3083', '\u3084', '\u3085', '\u3086', '\u3087', '\u3088', '\u3089', '\u308a', '\u308b', '\u308c', '\u308d', '\u308e', '\u308f', '\u3090', '\u3091', '\u3092', '\u3093', '\u30a1', '\u30a2', '\u30a3', '\u30a4', '\u30a5', '\u30a6', '\u30a7', '\u30a8', '\u30a9', '\u30aa', '\u30ab', '\u30ac', '\u30ad', '\u30ae', '\u30af', '\u30b0', '\u30b1', '\u30b2', '\u30b3', '\u30b4', '\u30b5', '\u30b6', '\u30b7', '\u30b8', '\u30b9', '\u30ba', '\u30bb', '\u30bc', '\u30bd', '\u30be', '\u30bf', '\u30c0', '\u30c1', '\u30c2', '\u30c3', '\u30c4', '\u30c5', '\u30c6', '\u30c7', '\u30c8', '\u30c9', '\u30ca', '\u30cb', '\u30cc', '\u30cd', '\u30ce', '\u30cf', '\u30d0', '\u30d1', '\u30d2', '\u30d3', '\u30d4', '\u30d5', '\u30d6', '\u30d7', '\u30d8', '\u30d9', '\u30da', '\u30db', '\u30dc', '\u30dd', '\u30de', '\u30df', '\u30e0', '\u30e1', '\u30e2', '\u30e3', '\u30e4', '\u30e5', '\u30e6', '\u30e7', '\u30e8', '\u30e9', '\u30ea', '\u30eb', '\u30ec', '\u30ed', '\u30ee', '\u30ef', '\u30f0', '\u30f1', '\u30f2', '\u30f3', '\u30f4', '\u30f5', '\u30f6']
		},{
			title: TXMSG('@specialchar.subtitle5'),
			options: ['\uff10', '\uff11', '\uff12', '\uff13', '\uff14', '\uff15', '\uff16', '\uff17', '\uff18', '\uff19', '\u2170', '\u2171', '\u2172', '\u2173', '\u2174', '\u2175', '\u2176', '\u2177', '\u2178', '\u2179', '\u2160', '\u2161', '\u2162', '\u2163', '\u2164', '\u2165', '\u2166', '\u2167', '\u2168', '\u2169', '\u0391', '\u0392', '\u0393', '\u0394', '\u0395', '\u0396', '\u0397', '\u0398', '\u0399', '\u039a', '\u039b', '\u039c', '\u039d', '\u039e', '\u039f', '\u03a0', '\u03a1', '\u03a3', '\u03a4', '\u03a5', '\u03a6', '\u03a7', '\u03a8', '\u03a9', '\u03b1', '\u03b2', '\u03b3', '\u03b4', '\u03b5', '\u03b6', '\u03b7', '\u03b8', '\u03b9\u03ba', '\u03bb', '\u03bc', '\u03bd', '\u03be', '\u03bf', '\u03c0', '\u03c1', '\u03c3', '\u03c4', '\u03c5', '\u03c6', '\u03c7', '\u03c8', '\u03c9']
		}]
	}
);

TrexMessage.addMsg({
	'@specialchar.cancel.image': "#iconpath/btn_l_cancel.gif?rv=1.0.1",
	'@specialchar.confirm.image': "#iconpath/btn_l_confirm.gif?rv=1.0.1",
	'@specialchar.title': "선택한 기호"
});
		
Trex.Tool.SpecialChar = Trex.Class.create({
	$const: {
		__Identity: 'specialchar'
	},
	$extend: Trex.Tool,
	oninitialized: function(config) {
			var _canvas = this.canvas;

			var _toolHandler = function(value) {
				if(!value){
					return;
				}
				_canvas.execute(function(processor) {
					processor.pasteContent(value, false);
				});
			};

			/* button & menu weave */
			this.weave.bind(this)(
				/* button */
				new Trex.Button(this.buttonCfg),
				/* menu */
				new Trex.Menu.SpecialChar(this.menuCfg),
				/* handler */
				_toolHandler
			);
		}
	
});

Trex.MarkupTemplate.add(
	'menu.specialchar.input', [
		'<dl class="tx-menu-matrix-input">',
		'	<dt><span>@specialchar.title</span></dt>',
		'	<dd><input type="text" value=""/></dd>',
		'	<dd><img class="tx-menu-btn-confirm" src="@specialchar.confirm.image" align="absmiddle"/></dd>',
		'	<dd><img class="tx-menu-btn-cancel" src="@specialchar.cancel.image" align="absmiddle"/></dd>',
		'</dl>'
	].join("")
);
Trex.Menu.SpecialChar = Trex.Class.create({
	$extend: Trex.Menu.Matrix,
	ongenerated: function(config) {
		var _elMenu = this.elMenu;
		
		var _elInputSet = Trex.MarkupTemplate.get('menu.specialchar.input').evaluateAsDom({});
		$tom.append($tom.collect(_elMenu, 'div.tx-menu-inner'), _elInputSet);

		var _elInput = this.elInput = $tom.collect(_elInputSet, 'input');
		var _elImgs = $tom.collectAll(_elInputSet, 'img');
			
		if(_elImgs.length == 2) {
			$tx.observe(_elImgs[0], "click", function() {
				this._command(this.elInput.value);
				this.hide();
			}.bind(this));
			$tx.observe(_elImgs[1], "click", function() {
				this.onCancel();
			}.bind(this));
		}
		
		$tx.observe( _elInput, "keydown", function(ev){
			if ( ev.keyCode == 13 ){
				$tx.stop(ev);
				this._command(this.elInput.value);
				this.hide();
			};
		}.bind(this));
	},
	onregenerated: function(config) {
		this.elInput.value = "";
		this.elInput.focus();
	},
	onSelect: function(ev) {
		var el = $tx.findElement(ev, 'span');
		if (el.tagName && el.tagName.toLowerCase() != 'span') {
			return;
		}
		this.elInput.value += (!el.innerText || el.innerText == "&nbsp;" || el.innerText.trim() == "")? "": el.innerText;
		$tx.stop(ev);
	}
});
