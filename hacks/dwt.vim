" Vim syntax file
" Language:	Dreamweaver Infested HTML
" Maintainer:	Aaron Brady <bradya@gmail.com>
" URL:		http://insom.me.uk/05/dwt.vim
" Last change:	2005 Jul 20

" For version 5.x: Clear all syntax items
" For version 6.x: Quit when a syntax file was already loaded
if version < 600
  syntax clear
elseif exists("b:current_syntax")
  finish
endif

if !exists("main_syntax")
  let main_syntax = 'dwt'
endif

" Next syntax items are case-sensitive
syn case match

" Include HTML syntax
syn include @dwtHtml <sfile>:p:h/php.vim

syn region editableRegion matchgroup=editableTag start=/<!-- InstanceBeginEditable name=".*" -->/  keepend end=/<!-- InstanceEndEditable -->/ contains=@dwtHtml
" Define the default highlighting.
" For version 5.7 and earlier: only when not done already
" For version 5.8 and later: only when an item doesn't have highlighting yet
if version >= 508 || !exists("did_dwt_syn_inits")
  if version < 508
    let did_dwt_syn_inits = 1
    command -nargs=+ HiLink hi link <args>
  else
    command -nargs=+ HiLink hi def link <args>
  endif
  delcommand HiLink
endif

if main_syntax == 'dwt'
  unlet main_syntax
endif

let b:current_syntax = "dwt"

" vim: ts=8
