/**
 * @imageoverview 
 * Image 업로드 관련 Source
 * Trex.Tool.Image - UI,
 * Trex.Attacher.Image,
 * Trex.Attachment.Image,
 * default configuration를 포함하고 있다.
 */
TrexConfig.addTool(
	"image",
	{
		wysiwygonly: true,
		sync: false,
		status: false
	}
);

TrexMessage.addMsg({
	'@image.title': "사진"
});

Trex.Tool.Image = Trex.Class.create({
	$const: {
		__Identity: 'image'
	},
	$extend: Trex.Tool,
	oninitialized: function(config) {
		var _editor = this.editor;
		this.weave.bind(this)(
			new Trex.Button(this.buttonCfg), 
			null,
			function() {
				_editor.getSidebar().getAttacher("image").execute();
			}
		);
	}
});

TrexConfig.addAttacher(
	"image",
	{	
		multiple: true,
		multipleuse: false,
		checksize: false,
		boxonly: false,
		wysiwygonly: true,
		objattr: {},
		features: { left:250, top:65, width:797, height:644 },
		popPageUrl: "#host#path/pages/popup/image.html"
	},
	function(root){
		var _config = TrexConfig.getAttacher("image", root);
		_config.popPageUrl = TrexConfig.getUrl(_config.popPageUrl);
		_config.features = TrexConfig.getPopFeatures(_config.features);
	}
);

/**
 * Trex.Attacher.Image
 * @class
 * @extends Trex.Attacher
 */
Trex.Attacher.Image = Trex.Class.create({
	$const: {
		__Identity: 'image'
	},
	$extend: Trex.Attacher,
	name: 'image',
	title: TXMSG("@image.title"),
	canModified: false,
	canResized: true,
	oninitialized: function(root) {
		
	},
	getKey: function(data) {
		return data.imageurl;
	},
	getDataForEntry: function(data) {
		data.imageurl = this.encodeSpaceInUrl(data.imageurl);
		data.originalurl = this.encodeSpaceInUrl(data.originalurl);
		data.attachurl = this.encodeSpaceInUrl(data.attachurl);
		  
		if(!data.dispElId) {
			data.dispElId = Trex.Util.getDispElId();
		}
		var _seq = ((data.tmpSeq)? this.entryBox.syncSeq(data.tmpSeq): this.entryBox.newSeq());
		var _data = Object.extend({ 
			dataSeq: _seq
		}, data); //NOTE: Cuz IE
		return _data;
	},
	createEntry: function(data, type) {
		return this.createAttachment(data, type);
 	},
	encodeSpaceInUrl: function(url){
		if ( !url ) {
			return ;
		}
		
		return url.replace(/ /g, "%20");	
	},
	execAttach: function(data, type) {
		var _entry = this.createEntry(this.getDataForEntry(data), type);
		_entry.execRegister();
	},
	execReload: function(data, content, type) {
		var _entry = this.createEntry(this.getDataForEntry(data, content), type);
		_entry.execReload();
	}
});

/**
 * Trex.Attachment.Image 
 * 
 *  @example
 *  	data = {
 *			thumburl: "string",
 *			imageurl: "string",
 *			filename: "string",
 *			filesize: number
 *		}
 * @class
 * @extends Trex.Attachment
 */
Trex.Attachment.Image = Trex.Class.create({
	$const: {
		__Identity: 'image'
	},
	$extend: Trex.Attachment,
	getFieldAttr: function(data) {
		return {
			name: 'tx_attach_image', 
			value: [data.thumburl, data.imageurl, data.originalurl, data.exifurl, data.filename, data.filesize].join('|')
		};
	},
	getBoxAttr: function(data) {
		var _rectangle = data.width ? data.width + "x" + data.height + " / " : ""; 
		return {
			name: data.filename + " (" +  _rectangle + data.filesize.toByteUnit() + ")",
			image: data.thumburl
		};
	},
	getObjectAttr: function(data) {
		var _objattr = Object.extend({}, this.actor.config.objattr);
		if(data.width) {
			if(!_objattr.width || _objattr.width > data.width) {
				_objattr.width = data.width;
			}
		} else {
			_objattr.width = null;
		}
		if(data.height) {
			if(!_objattr.height || _objattr.height > data.height) {
				_objattr.height = data.height;
			}
		} else {
			_objattr.height = null;
		}
		return _objattr;
	},
	getObjectStyle: function(data) {
		var _objstyle = {};
		if(this.actor.config.objstyle) {
			_objstyle = Object.extend(_objstyle, this.actor.config.objstyle);
		}
		if(data.imagealign) {
			var _objectStyle = {
				"L": Trex.Tool.AlignLeft,
				"C": Trex.Tool.AlignCenter,
				"FL": Trex.Tool.AlignRight,
				"FR": Trex.Tool.AlignFull
			}[data.imagealign];
			if (_objectStyle && _objectStyle.__ImageModeProps && _objectStyle.__ImageModeProps['image']) {
				_objstyle = Object.extend(_objstyle, _objectStyle.__ImageModeProps['image']['style']);
			}
		}
		return _objstyle;
	},
	getParaStyle: function(data) {
		var _parastyle = Object.extend({}, this.actor.config.parastyle || this.actor.config.defaultstyle);
		if(data.imagealign) {
			var _objectStyle = {
				"L": Trex.Tool.AlignLeft,
				"C": Trex.Tool.AlignCenter,
				"FL": Trex.Tool.AlignRight,
				"FR": Trex.Tool.AlignFull
			}[data.imagealign];
			if (_objectStyle && _objectStyle.__ImageModeProps && _objectStyle.__ImageModeProps['paragraph']) {
				_parastyle = Object.extend(_parastyle, _objectStyle.__ImageModeProps['paragraph']['style']);
			}
		}
		return _parastyle;
	},
	getSaveHtml: function(data) {
		return "<img src=\"" + data.imageurl + "\" class=\"tx-daum-image\"/>";
	},
	getDispHtml: function(data) {
		return "<img id=\"" + data.dispElId + "\" src=\"" + data.imageurl + "\" class=\"txc-image\"/>";
	},
	getDispText: function(data) {
		return "<img src=\"" + data.imageurl + "\" class=\"tx-daum-image\"/>";
	},
	getRegLoad: function(data) {
		return new RegExp("<(?:img|IMG)[^>]*src=\"?" + data.imageurl.getRegExp() + "\"?[^>]*\/?>", "gm");
	},
	getRegHtml: function(data) {
		return new RegExp("<(?:img|IMG)[^>]*src=\"?" + data.imageurl.getRegExp() + "\"?[^>]*\/?>", "gm");
	}, 
	getRegText: function(data) {
		return new RegExp("<(?:img|IMG)[^>]*src=\"?" + data.imageurl.getRegExp() + "\"?[^>]*\/?>", "gm");
	}
});
